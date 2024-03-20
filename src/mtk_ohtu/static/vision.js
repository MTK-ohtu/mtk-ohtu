import { createListElement, createMarker, runListElementAnimation, addToListElement } from './element_factory.js'

// This unit deals with objects called features. To add new features to vision controller, one needs to call for 
// 'addFeatureToGroup' (single)or 'addFeaturesToGroup (list of features)'. Features are geoJSON objects.
// This unit also accepts geoJSON objects called 'FeatureCollection'. One collection has a field 'features'
// having list of single features as value.


class VisionController {

    constructor(leaflet, map) {
        this.padding = 0.1
        this.L = leaflet
        this.map = map
        this.data = {
                                        // Abbreviations:   CL = contractor location id
                                        //                  CLF = one feature related to one contractor location

            popup_open: {},             // For each CL, remember if corresponding marker's popup is open or not
                                        // Key: feature.properties.location_id
            
            element_open: {},           // -**-, remember if corresponding list element is open or not
                                        // Key: feature.properties.location_id

            category: {},               // For every category (can process etc.) mark down given value for every CLF
                                        // Key: JSON.stringify(feature)
            
            group: {},                  // For each CL, keep record of it's current groupname ('optimal' etc.)
                                        // Key: feature.properties.location_id OR route.metadata.timestamp
                                        // NOTE: group name is used as a style class, so check from style.css that they're the same
            
            group_icon: {},             // For each group, remember their icon
                                        // Key: group name
            
            element: {},                // For each CL, remember their corresponding list element (created in element_factory.js)
                                        // Key: feature.properties.location_id
            
            map_object: {},             // For each feature, remember their corresponding leaflet-object. (can be marker, geojson...)
                                        // Key: feature.properties.location_id OR route.metadata.timestamp
            
            object_type: {},            // For every feature, remember their type (just marker, l_marker = marker+list element combo)
                                        // Key: feature.properties.location_id OR route.metadata.timestamp
            
            bounds: {},                 // For every map object, remember their corresponding latLngBounds value on leaflet
                                        // Key: feature.properties.location_id OR route.metadata.timestamp
            
            in_focus: {},               // For every feature, keep record wether their bounds will be considered in calculation of total bounds
                                        // Key: feature.properties.location_id OR route.metadata.timestamp
            
            visible: {},                // For every feature, keep record of their current visibility status
                                        // Key: feature.properties.location_id OR route.metadata.timestamp
            
            group_visible: {},          // For every group, keep record of their current visibility status
                                        // Key: group name
            
            filtered: {},               // For every CL, keep record of how many active filters they are affected by
                                        // Key: feature.properties.location_id
            
            service_home: {}            // For every CLF, remember their CL. This removes the need to use JSON.parse in every query
                                        // Key: JSON.stringify(feature) 
        }

        //These are used in controller logic
        this.zoomedFeature = null
        this.openFeature = null
        this.focusedRoute = null
        this.send = false
        this.companyFocus = true
        this.flyTransition = 'normal'

        //Bind one proxy to every data subdirectory. There will be one for every subdirectory, but they may not be used.
        this.proxies = {};
        for (const key in this.data) {
            this.proxies[key] = this.getProxy(this.data[key], key);
        }

        // NOTE: when calling .proxy instead of .data, proxy will update value in 'data' AND after that,
        // it will notify visionController. This will trigger an effect on GUI. See featured effects below.
    }

    //=========================================================================================== VISION CONTROL
    //When notified about change, change visuals according to the new state
    visionController(note) {
        console.log("visionController === '"+note.key+": '"+note.property+"' -> "+note.value)
        var attribute = note.key
        var id = note.property
        var value = note.value

        //=======================================ELEMENT CLOSE/OPEN
        if (attribute == 'element_open') {
            if (value) {
                if (this.openFeature != null) {
                    runListElementAnimation(this.data.element[this.openFeature], 1)
                    this.data.element_open[this.openFeature] = false
                    this.proxies.popup_open[this.openFeature] = false
                    if (this.zoomedFeature != null) { 
                        this.data.element[this.openFeature].querySelector('#zoom_button')
                            .classList.remove('zoomed_in')
                        this.data.element[id].querySelector('#zoom_button')
                            .classList.add('zoomed_in')   
                        this.zoomedFeature = id
                    }
                }
                this.openFeature = id
                runListElementAnimation(this.data.element[id], 2)
            } else {
                runListElementAnimation(this.data.element[id], 1)
                if (this.focusedRoute == null) this.flyTransition = 'none'
                this.openFeature = null
                if (this.zoomedFeature != null) {
                    this.data.element[id].querySelector('#zoom_button')
                            .classList.remove('zoomed_in')
                    this.zoomedFeature = null
                }
            }
            this.fly()
        }

        //=======================================POPUP CLOSE/OPEN
        if (attribute == 'popup_open') { 
            var marker = this.data.map_object[id]
            if (value) marker.openPopup()
            else marker.closePopup()
        }

        //=======================================CHECK FILTER VALUE
        if (attribute == 'filtered') {
            this.data.element[id].classList.remove(this.data.group[id])
            if (value <= 0) {
                this.proxies.group[id] = 'suboptimal'
            } else {
                this.proxies.group[id] = 'optimal'
            }
        }

        //=======================================SET VISIBLE / HIDDEN
        if (attribute == 'visible') {
            var count = document.getElementById('company_count')
            var type = this.data.object_type[id]
            if (type == 'l_marker') count.textContent = parseInt(count.textContent)+ ((-1)+2*(value ? 1 : 0))
            if (value) {
                this.data.map_object[id].addTo(this.map)
                if (type == 'l_marker') {
                    this.data.element[id].style.display = 'block'
                    this.proxies.in_focus[id] = true
                    runListElementAnimation(this.data.element[id], 1)
                }
            }
            else {
                this.map.removeLayer(this.data.map_object[id])
                if (type == 'l_marker') {
                    if (this.openFeature == id) {
                        console.log("OpenFeature: "+this.openFeature)
                        this.openFeature = null
                    }
                    this.proxies.in_focus[id] = false
                    this.data.popup_open[id] = false
                    this.data.element_open[id] = false
                    runListElementAnimation(this.data.element[id], 0)
                    this.data.element[id].addEventListener('animationend', () => {
                        this.data.element[id].style.display = 'none'
                    }, { once: true })
                }
            }
        }

        //=======================================ADD/REMOVE FOCUS
        if (attribute == 'in_focus') {
            if (this.data.object_type[id] === 'route') {
                if (this.focusedRoute === null) {
                    this.focusedRoute = id
                } else {
                    this.focusedRoute = null
                }
            }
            this.fly()
        }

        //======================================MOVE FEATURE TO GROUP
        if (attribute == 'group') {
            var marker = this.data.map_object[id]
            marker.setIcon(this.data.group_icon[value])
            var element = this.data.element[id]
            element.classList.add(this.data.group[id])            
            var type = this.data.object_type[id]
            if (!this.data.visible[id] && this.data.group_visible[value]) {
                this.proxies.visible[id] = true
                this.proxies.in_focus[id] = true
            }
            else if (this.data.visible[id]) {
                if (!this.data.group_visible[value]) {
                    this.proxies.visible[id] = false
                    this.proxies.in_focus[id] = false    
                }
            }
        }
    }
    //New proxy for reporting changes in data
    getProxy(subdata, key) {
        const self = this
        return new Proxy(subdata, {
            set (target, property, value){
                target[property] = value
                self.visionController({key:key, target:target, property:property, value:value})
                return true
        }})
    }
    
    //=============================================================================== ADD
    addListFeaturesToGroup(features, group_name, icon) {
        this.data.group_icon[group_name] = icon
        this.data.group_visible[group_name] = true
        features.forEach(feature => {
            this.addListFeatureToGroup(feature, group_name, icon)
        })
    }
    
    // Features are contractor location related JSON objects. EXPECTED fields in single feature are:
    //
    // 'geometry': { 'coordinates': [FLOAT (longitude), FLOAT (latitude)] }}
    // 'properties': {}, containing named fields:
    // address, name, location_id, email, telephone, base_rate, price_per_km, max_capacity, unit, can_process

    addListFeatureToGroup(feature, group_name, icon) {
        this.addListFeatureToCategories(feature)
        const f = feature.properties.location_id
        console.log("Added list-feature: "+f)
        this.data.popup_open[f] = false
        this.data.element_open[f] = false
        this.data.group[f] = group_name
        if (this.data.element.hasOwnProperty(f)) {
            addToListElement(this.data.element[f], feature)
            this.data.filtered[f] += 1
        } else {
            this.data.element[f] = createListElement(feature, group_name)
            this.setEventListener(this.data.element[f])
            this.data.map_object[f] = createMarker(feature, icon, this.L)
            this.setMarkerClick(this.data.map_object[f], f)
            const c = feature.geometry.coordinates
            this.data.bounds[f] = L.latLngBounds(
                L.latLng(c[1]-this.padding, c[0]-this.padding),
                L.latLng(c[1]+this.padding, c[0]+this.padding)
            )
            this.data.object_type[f] = 'l_marker'
            this.data.in_focus[f] = true
            this.proxies.visible[f] = true
            this.data.filtered[f] = 1
        }
    }

    addMapFeatureToGroup(feature, group_name, icon) {
        const f = feature.properties.address
        console.log("Added map-feature: "+f)
        if (!this.data.group_visible.hasOwnProperty(group_name)) {
            this.data.group_visible[group_name] = true
        }
        this.data.group[f] = group_name
        this.data.map_object[f] = createMarker(feature, icon, this.L)
        const c = feature.geometry.coordinates
        this.data.bounds[f] = L.latLngBounds(
            L.latLng(c[1], c[0]),
            L.latLng(c[1], c[0])
        )
        this.data.object_type[f] = 'marker'
        this.data.in_focus[f] = true
        this.proxies.visible[f] = true
    }

    addRoutesToGroup(routes, group_name) {
        routes.forEach(route => {
            this.addRoute(route, group_name)
        })
    }

    addRouteToGroup(route, group_name) {
        var routeId = route.metadata.timestamp
        var [lngmin, latmin, lngmax, latmax] = route.bbox
        this.data.bounds[routeId] = 
            this.L.latLngBounds(
                this.L.latLng(latmin, lngmin),
                this.L.latLng(latmax, lngmax)
            )
        this.data.map_object[routeId] = L.geoJSON(route)
        this.data.in_focus[routeId] = false
        this.data.object_type[routeId] = 'route'
        this.data.group[routeId] = group_name
        this.proxies.visible[routeId] = false
    }

    addListFeatureToCategories(feature) {
        this.data.service_home[JSON.stringify(feature)] = feature.properties.location_id
        Object.entries(feature.properties).forEach(([key,value]) => {
            if (!this.data.category.hasOwnProperty(key)) {
                this.data.category[key] = {}
            }
            this.data.category[key][JSON.stringify(feature)] = value
        })
    }
    //============================================================================== TOGGLE FILTER
    filterBy(property, value) {
        var list = Object.entries(this.data.category[property])
        if (typeof(value) === 'boolean') {
            list.filter(([key, val]) => val == false)
                .forEach(([key, val]) => {
                    this.proxies.filtered[this.data.service_home[key]] -= ((-1)+2*(value ? 1 : 0))
                })
        }
        if (typeof(value) === 'number') {
            list.forEach(([key, val]) => {
                this.data.filtered[this.data.service_home[val]] += 1;
            })
            // Non positive value means that value*(-1) is LOWER LIMIT (e.g max_capacity)
            if (value <= 0) {
                //Choose every feature, that has this property value less or equal
                list.filter(([key, val]) => val <= -value)
                    .forEach(([key, val]) => {
                        // Reduce the home location's filter value for every feature on list
                        this.data.filtered[this.data.service_home[val]] -= 1;
                    })
            }
            // Positive value means that value is UPPER LIMIT (e.g. base_rate)
            if (value > 0) {
                //Choose every feature, that has this property value over
                list.filter(([key, val]) => val > value)
                    .forEach(([key, val]) => {
                        // Reduce the home location's filter value for every feature on list
                        this.data.filtered[this.data.service_home[val]] -= 1;
                    })
            }
        }
    }
    //============================================================================== TOGGLE
    //List element is being clicked (call from listelement)
    toggleListElement(id) {
        var is_open = !Boolean(this.data.popup_open[id])
        this.proxies.popup_open[id] = is_open
        this.proxies.element_open[id] = is_open
    }

    toggleMarker(id) {
        this.flyTransition = 'none'
        this.toggleListElement(id)
    }

    //When zoom button is being pressed (call from listelement#zoom_button)
    toggleZoom(id) {
        this.flyTransition = 'fast'
        if (this.zoomedFeature != null) {
            this.zoomedFeature = null
            this.data.element[id].querySelector('#zoom_button')
            .classList.remove('zoomed_in')
        } else {
            this.zoomedFeature = id
            this.data.element[id].querySelector('#zoom_button')
                .classList.add('zoomed_in')
        }
        this.fly()
    }

    //Show or hide group of features. Doesn't trigger flying effect
    toggleGroupVisibility(group_name) {
        this.send = true
        const entries = Object.entries(this.data.visible)
            .filter(([key, value]) => this.data.group[key] === group_name)
            .map(([key, value]) => key)
        const last = entries.length -1
        var is_visible = !Boolean(this.data.group_visible[group_name])
        this.data.group_visible[group_name] = is_visible
        entries.forEach((key, index) => {
            // If group has an open element, it will be closed
            if (index == last) this.send = false
            // Change both visible and in_focus value of the feature
            this.proxies.in_focus[key] = is_visible 
            this.proxies.visible[key] = is_visible
        })
        this.send = false
    }

    //Add/remove focus on visible group. Triggers flying effect when all values updated.
    toggleGroupFocus(group_name) {
        this.send = true
        const entries = Object.entries(this.data.group)
            .filter(([key, value]) => value === group_name)
            .filter(([key, value]) => this.data.visible[key] == true)
            .map(([key, value]) => key)
        const last = entries.length -1
        entries.forEach((key, index) => {
            if (index == last) this.send = false
            this.proxies.in_focus[key] = !this.data.in_focus[key]
        })
        this.send = false
    }

    //Set focus on all visible l_markers
    addFocusOnVisibleListElements() {
        this.send = true
        const entries = Object.entries(this.data.visible)
            .filter(([key, value]) => this.data.visible[key])
            //.filter(([key, value]) => this.data.object_type[key] == 'l_marker')
            .map(([key, value]) => key)
        const last = entries.length -1;
        entries.forEach((key, index) => {
            if (index == last) this.send = false
            this.proxies.in_focus[key] = true
        })
        this.send = false
    }

    //Toggle forced focus on companies
    toggleCompanyFocus() {
        this.companyFocus = !this.companyFocus
        this.fly()
    }

    //============================================================================= MAP FLYER
    //Get bounds of all objects that are set to be in focus
    getInFocusBounds() {
        const list = Object.entries(this.data.bounds)
            .filter(([key, value]) => this.data.in_focus[key])
            .map(([key, value]) => value);
        return this.boundsOf(list)
    }
    //Calculate bounds from given list of L.latLngBounds
    boundsOf(list) {
        var latList = []; var lngList = []
        list.forEach(b => {
            if (b != null) {
            latList.push(b._southWest.lat); lngList.push(b._southWest.lng)
            latList.push(b._northEast.lat); lngList.push(b._northEast.lng)
        }})
        if (lngList.length === 0) return null;
        return this.L.latLngBounds(
            this.L.latLng(Math.min(...latList), Math.min(...lngList)-0.2),
            this.L.latLng(Math.max(...latList)+0.2, Math.max(...lngList)+0.2)
        )
    }

    //Fly here
    fly() {
        // Don't fly if updates are still coming
        if (this.send) {
            return
        }
        var bounds
        // Case when zoomin has been toggled on
        if (this.zoomedFeature != null) bounds = this.data.bounds[this.zoomedFeature]
        
        else if (this.focusedRoute !== null && !this.companyFocus) {
            // Case when one list element is open
            if (this.openFeature != null) {
                bounds = this.boundsOf([this.data.bounds[this.focusedRoute], this.data.bounds[this.openFeature]])
            }
            //...or no list elements are open
            else bounds = this.data.bounds[this.focusedRoute]
        }
        // If focus is set on visible companies OR if no list element is open
        else if (this.companyFocus || this.openFeature == null){
            bounds = this.getInFocusBounds()
        }
        // Case when ending the zoomin feature
        else if (this.openFeature != null) {
            bounds = this.data.bounds[this.openFeature].pad(5)
        } 
        if (this.flyTransition == 'fast') this.map.fitBounds(bounds)
        else if (this.flyTransition == 'normal') this.map.flyToBounds(bounds)
        this.flyTransition = 'normal'        
    }

    //============================================================================= LISTENERS
    setEventListener(element) {
        element.addEventListener('click', (e) => {
            if (e.target.id === 'zoom_button') {
                var element = e.target.parentElement.closest('button')
                this.toggleZoom(element.id)
            } else {
                var element = e.target.closest('button')
                this.toggleListElement(element.id)
            }
        })
    }

    setMarkerClick(marker, id) {
        marker.on('click', (e) => {
            this.toggleMarker(id);
        });
    }
}

export { VisionController }