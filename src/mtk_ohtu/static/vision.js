import { createListElement, createMarker, runListElementAnimation } from './element_factory.js'

class VisionController {

    constructor(leaflet, map) {
        this.padding = 0.1
        this.L = leaflet
        this.map = map
        this.data = {
            popup_open: {},
            element_open: {},
            group: {},
            element: {},
            map_object: {},
            object_type: {},
            bounds: {},
            in_focus: {},
            visible: {}
        }
        this.proxies = {};
        this.zoomedFeature = null
        this.openFeature = null
        this.focusedRoute = null
        this.send = false
        this.companyFocus = false

        //Bind data subdirectories to corresponding proxies
        for (const key in this.data) {
            this.proxies[key] = this.getProxy(this.data[key], key);
        }

        //NOTE: when calling a proxy of 'data' (instead of just 'data') subdirectory, proxy will update value in 'data'
        //AND notify visionController. This will trigger an effect on GUI. See featured effects below.
    }

    //=========================================================================================== MASTER
    //When notified about change, change visuals according to new state
    visionController(note) {
        console.log("controlMaster === '"+note.key+": '"+note.property+"' -> "+note.value)
        var attribute = note.key
        var feature = note.property
        var value = note.value
        //=======================================ELEMENT CLOSE/OPEN
        if (attribute == 'element_open') {
            if (value) {
                if (this.openFeature != null) {
                    runListElementAnimation(this.data.element[this.openFeature])
                    this.data.element_open[this.openFeature] = false
                    this.proxies.popup_open[this.openFeature] = false
                    if (this.zoomedFeature != null) { 
                        this.data.element[this.openFeature].querySelector('#zoom_button')
                            .classList.remove('zoomed_in')
                        this.data.element[feature].querySelector('#zoom_button')
                            .classList.add('zoomed_in')   
                        this.zoomedFeature = feature
                    }
                }
                this.openFeature = feature
                runListElementAnimation(this.data.element[feature])
            } else {
                runListElementAnimation(this.data.element[feature])
                this.openFeature = null
                if (this.zoomedFeature != null) {
                    this.data.element[feature].querySelector('#zoom_button')
                            .classList.remove('zoomed_in')
                    this.zoomedFeature = null
                }
            }
            this.fly()
        }
        //=======================================POPUP CLOSE/OPEN
        if (attribute == 'popup_open') { 
            var marker = this.data.map_object[feature]
            if (value) marker.openPopup()
            else marker.closePopup()
        }
        //=======================================SET VISIBLE / HIDDEN
        if (attribute == 'visible') {
            var count = document.getElementById('company_count')
            var type = this.data.object_type[feature]
            if (type == 'l_marker') count.textContent = parseInt(count.textContent)+ ((-1)+2*(value ? 1 : 0))
            if (value) {
                this.data.map_object[feature].addTo(this.map)
                if (type == 'l_marker') this.data.element[feature].style.display = 'block'
            }
            else {
                this.map.removeLayer(this.data.map_object[feature])
                if (type == 'l_marker') this.data.element[feature].style.display = 'none'
            }
        }
        //=======================================ADD/REMOVE FOCUS
        if (attribute == 'in_focus') {
            if (this.data.object_type[feature] === 'route') {
                if (this.focusedRoute === null) {
                    this.focusedRoute = feature
                } else {
                    this.focusedRoute = null
                }
            }
            this.fly()
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
        features.forEach(feature => {
            this.addListFeatureToGroup(feature, group_name, icon)
        })
    }

    //Add list feature with corresponding marker on the map
    addListFeatureToGroup(feature, group_name, icon) {
        const f = feature.properties.address
        console.log("Added feature: "+f)
        this.data.popup_open[f] = false
        this.data.element_open[f] = false
        this.data.group[f] = group_name
        this.data.element[f] = createListElement(feature)
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
    }

    addMapFeatureToGroup(feature, group_name, icon) {
        const f = feature.properties.address
        console.log("Added feature: "+f)
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
        routes.forEach(feature => {
            this.addRoute(feature, group_name)
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

    //============================================================================== TOGGLE
    //List element is being clicked (call from listelement)
    toggleFeature(feature) {
        var is_open = !Boolean(this.data.popup_open[feature])
        this.proxies.popup_open[feature] = is_open
        this.proxies.element_open[feature] = is_open
    }

    //When zoom button is being pressed (call from listelement#zoom_button)
    toggleZoom(feature) {
        if (this.zoomedFeature != null) {
            this.zoomedFeature = null
            this.zoomOutTransition = true
            this.data.element[feature].querySelector('#zoom_button')
            .classList.remove('zoomed_in')
        } else {
            this.zoomedFeature = feature
            this.data.element[feature].querySelector('#zoom_button')
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
        entries.forEach((key, index) => {
            var is_visible = !Boolean(this.data.visible[key])
            // If group has an open element, it will be closed
            if (this.data.element_open[key]) this.toggleFeature(key)
            if (index == last) this.send = false
            // Change both visible and in_focus value of the feature
            this.proxies.in_focus[key] = is_visible 
            this.proxies.visible[key] = is_visible
        })
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
    }

    //Focus on all visible markers
    addFocusOnVisibleListElements() {
        this.send = true
        const entries = Object.entries(this.data.visible)
            .filter(([key, value]) => this.data.visible[key])
            .filter(([key, value]) => this.data.object_type[key] == 'l_marker')
            .map(([key, value]) => key)
        const last = entries.length -1;
        entries.forEach((key, index) => {
            if (index == last) this.send = false
            this.proxies.in_focus[key] = true
        })
    }

    toggleCompanyFocus() {
        if (this.companyFocus) {
            this.companyFocus = false
        } else {
            this.companyFocus = true
        }
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
        if (this.send) return
        // Case when zoomin has been toggled on
        if (this.zoomedFeature != null) {
            this.map.fitBounds(this.data.bounds[this.zoomedFeature])
        } 
        // Case when route focus is toggled on
        else if (this.focusedRoute !== null && !this.companyFocus) {
            // Case when one list element is open
            if (this.openFeature != null) {
                this.map.flyToBounds(this.boundsOf([
                    this.data.bounds[this.focusedRoute], this.data.bounds[this.openFeature]
                ]))
            }
            //...or no list elements are open
            else {
                this.map.flyToBounds(this.data.bounds[this.focusedRoute])
            }
        }
        else if (this.companyFocus || this.openFeature == null){
            this.map.flyToBounds(this.getInFocusBounds())
        }
        // Case when ending the zoomin feature
        else if (this.openFeature != null) {
            this.map.flyToBounds(this.data.bounds[this.openFeature].pad(5))
        }
        // Otherwise just focus on everything in_focus
        
    }

    //============================================================================= LISTENERS
    setEventListener(element) {
        element.addEventListener('click', (e) => {
            if (e.target.id === 'zoom_button') {
                var element = e.target.parentElement.closest('button')
                this.toggleZoom(element.id)
            } else {
                if (e.target.tagName === 'BUTTON') {
                    var element = e.target
                } else {
                    var element = e.target.closest('button')
                }
                this.toggleFeature(element.id)
            }
        })
    }

    setMarkerClick(marker, feature) {
        marker.on('click', (e) => {
            this.toggleFeature(feature);
        });
    }
}

export { VisionController }