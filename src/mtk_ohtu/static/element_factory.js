
// var runListElementAnimation = function (element, state, target) {
    
    
//     if (element.classList.contains('visible')) {
//         element.classList.remove('visible')
//         var from = 1
//     }
//     if (element.classList.contains('closed')) {
//         element.classList.remove('closed')
//         var from = 1
//     }
//     if (element.classList.contains('open')) {
//         element.classList.remove('open')
//         var from = 2
//     }
//     else {
//         element.classList.remove('vanished')
//         var from = 0
//     }
    
//     console.log("Animate element "+element.id+": "+from+" -> "+state)

//     if (target == 'info') {
//         document.getElementById('blank').style.display = 'block'
//         element.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest'});
//     } 
//     else if (target == 'map'){
//         element.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest'});
//     } 

//     if (state == 0) {
//         console.log("Vanishing element "+element.id)
//         element.style.setProperty('--lower-height', '0%')
//         if (from == 2) {
//             element.style.setProperty('--upper-height', element.style.getPropertyValue('--open-height'))//element.scrollHeight+'px')
//         }
//         else {
//             element.style.setProperty('--upper-height',  element.style.getPropertyValue('--closed-height'))//element.querySelector('div').scrollHeight+'px')
//         }
//         element.classList.add('vanished')
//         element.classList.remove('selected')

//     } else if (state == 1) {
//         console.log("To closed state: element "+element.id)
//         if (from == 2) {
//             if (target == 'info') element.querySelector('div').style.minHeight = '100%'
//             element.style.setProperty('--lower-height',  element.style.getPropertyValue('--closed-height'))//element.querySelector('div').scrollHeight+'px')
//             element.style.setProperty('--upper-height',  element.style.getPropertyValue('--open-height'))//element.scrollHeight-25+'px')
//             element.classList.add('closed')
//             element.classList.remove('selected')
//         }
//         else {
//             element.style.setProperty('--lower-height', '0%')
//             element.style.setProperty('--upper-height',  element.style.getPropertyValue('--closed-height'))//element.querySelector('div').scrollHeight+'px')
//             element.classList.add('visible')
//         }

//     } else {
//         console.log("Opening element "+element.id)
//         console.log(element.className+": Closed: "+  element.style.getPropertyValue('--closed-height') 
//                         +"%, Open:"+ element.style.getPropertyValue('--open-height')+"%")
//         console.log(element.className+": upper: "+  element.style.getPropertyValue('--upper-height') +"%, lower:"
//                         + element.style.getPropertyValue('--lower-height')+"%")
//         if (target == 'info') element.querySelector('div').style.minHeight = '0%'
//         element.style.setProperty('--lower-height',  element.style.getPropertyValue('--closed-height'))//element.querySelector('div').scrollHeight+'px')
//         element.style.setProperty('--upper-height',  element.style.getPropertyValue('--open-height'))//element.scrollHeight+'px')
//         console.log(element.className+": upper: "+  element.style.getPropertyValue('--upper-height') +"%, lower:"
//                         + element.style.getPropertyValue('--lower-height')+"%")
//         element.classList.add('selected')
//         element.classList.add('open')
//     }
//     console.log("Element "+element.id+": --")
//     document.getElementById('blank').style.display = 'none'
// }   
var runListElementAnimation = function (element, state, target) {
    element.style.setProperty('--from-height', element.style.getPropertyValue('--to-height'))
    console.log("Element "+element.id+" FROM "+ element.style.getPropertyValue('--from-height'))
    if (target == 'map'){
        element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest'});
    } 

    if (state == 0) {
        // console.log("Vanishing element "+element.id)
        element.style.setProperty('--to-height', '0%')
        element.classList.remove('selected')
        element.classList.add('hidden')

    } else if (state == 1) {
        console.log("To closed state: element "+element.id)
        if (target == 'info') element.querySelector('div').style.minHeight = '100%'
        element.style.setProperty('--to-height', element.style.getPropertyValue('--closed-height'))
        element.classList.remove('selected')
        element.classList.remove('hidden')

    } else {
        console.log("Opening element "+element.id)
        if (target == 'info') element.querySelector('div').style.minHeight = '33%'
        element.style.setProperty('--to-height', element.style.getPropertyValue('--open-height'))
        element.classList.add('selected')
        element.classList.remove('hidden')
    }
    // console.log("Element "+element.id+" TO "+ element.style.getPropertyValue('--to-height'))
    
    if (element.classList.contains('animate-open')){
        element.classList.remove('animate-open')
        element.classList.add('animate-closed')
    }
    else {
        element.classList.remove('animate-closed')
        element.classList.add('animate-open')
    }
}  

// Create elements to show on the list side ====================================================================
function createListElement(feature, styleClass, container) {
    var listElement = document.createElement('div');
    listElement.id = feature.properties.location_id
    listElement.innerHTML = `
        <div class="horizontal-container even"> 
            <h4>${feature.properties.name}</h4>
            <p style="text-align: right;">${feature.properties.address}</p>
        </div>
        <div id="info">
            <div class="horizontal-container even">
                <h4>${feature.properties.email}</h4>
                <h4>${feature.properties.telephone}</h4>
                <button type="button" class="zoom_button" id="zoom_button"></button>
            </div>
            
            <div class="horizontal-container" style="align-items: flex-start; margin-top: 3%">
                <h4>${document.getElementById('services').textContent}:</h4>
                <div>
                    <div id="services">
                    </div>
                </div>
            </div>
            <div class="horizontal-container" style="gap: 5%">
                <h4>${document.getElementById('description').textContent}:</h4>
                <p>Kuljetusyritys</p>
            </div>
        </div>
        <div style="height: 10px;"></div>
        `;
    
    container.appendChild(listElement)
    listElement.querySelector('#services').appendChild(createServiceElement(feature))
    listElement.classList.add('clickable_list_element');
    
    if (typeof styleClass !== 'undefined') {
        console.log("Lisätään elementille "+listElement.id+" luokka "+styleClass)
        listElement.classList.add(styleClass)
    }

    listElement.style.setProperty('--closed-height',
        (listElement.querySelector('div').scrollHeight/ listElement.parentNode.clientHeight)*100 + '%')
    const childSum = Array.from(listElement.children)
            .map(child => child.scrollHeight)
            .reduce((acc, val) => acc + val, 0);
    listElement.style.setProperty('--open-height',
        (childSum/ listElement.parentNode.clientHeight)*100 + '%')
    console.log("LISTDIV HEIGHT: "+listElement.parentNode.scrollHeight)
    listElement.style.setProperty('--from-height', '0%')
    listElement.style.setProperty('--to-height', listElement.style.getPropertyValue('--closed-height'))
    listElement.classList.add('animated');
        
    return listElement

} // ==============================================================================================

function addToListElement(element, feature) {
    console.log("Elementti "+feature.properties.address+" sisälsi jo yhden elementin")
    console.log(element.querySelector('#services'))
    element.querySelector('#services').appendChild(createServiceElement(feature))
    element.style.setProperty('--open-height',
        (element.scrollHeight/ element.parentNode.clientHeight)*100 + '%')
}

function createServiceElement(feature) {
    var serviceElement = document.createElement('div')
    serviceElement.classList.add('service_element')
    serviceElement.id = JSON.stringify(feature)
    serviceElement.innerHTML = `
            <button type="button" id="service_car" class="car_info"></button>
            <button type="button" id="cargo_rate" class="rate_info">
                <h2 style="padding: 0px; margin: 0px; font-size: 1.3vh;">${feature.properties.base_rate}/${feature.properties.price_per_km}e</h2>
            </button>
            <button type="button" id="cargo_weight" class="cargo_weight_info">
                <p style="font-size: 1.4vh;">${feature.properties.max_capacity} ${feature.properties.unit}</p>
            </button>
            ${feature.properties.can_process ? '<button type="button" id="can_process" class="handle_info"></button>' : ''}
    `;
    return serviceElement
}

//Returns a function which is to be used as 'pointToLayer' function in leaflet. Creates marker popup.
function createMarker(feature, icon, L) {
    var [lat, lng] = feature.geometry.coordinates
    var marker = L.marker(L.latLng(lng, lat), { icon: icon })
    var popup = new L.popup({ autoClose: false, closeOnClick: false }).setContent(
        '<h4>' + feature.properties.name + '</h4><p>' + feature.properties.address+'</p><p>' + lat+','+lng+'</p>'
        )
    popup._initLayout()
    marker.i = feature.properties.location_id
    marker.bindPopup(popup);
    return marker;
}

export { createListElement, createMarker, runListElementAnimation, addToListElement }