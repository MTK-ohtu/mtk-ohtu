
var runListElementAnimation = function (element, state) {
    if (element.classList.contains('vanished')) {
        element.classList.remove('vanished')
        var from = 0
    }
    if (element.classList.contains('visible')) {
        element.classList.remove('visible')
        var from = 1
    }
    if (element.classList.contains('closed')) {
        element.classList.remove('closed')
        var from = 1
    }
    if (element.classList.contains('open')) {
        element.classList.remove('open')
        var from = 2
    }
    if (state == 0) {
        element.style.setProperty('--lower-height', '0px')
        if (from == 2) {
            element.style.setProperty('--upper-height', element.scrollHeight+'px')
        }
        else {
            element.style.setProperty('--upper-height', element.querySelector('div').scrollHeight+'px')
        }
        element.classList.add('vanished')
        element.classList.remove('selected')

    } else if (state == 1) {
        if (from == 2) {
            element.style.setProperty('--lower-height', element.querySelector('div').scrollHeight+'px')
            element.style.setProperty('--upper-height', element.scrollHeight-25+'px')
            element.classList.add('closed')
            element.classList.remove('selected')
        }
        else {
            element.style.setProperty('--lower-height', '0px')
            element.style.setProperty('--upper-height', element.querySelector('div').scrollHeight+'px')
            element.classList.add('visible')
        }
    } else {
        element.style.setProperty('--lower-height', element.querySelector('div').scrollHeight+'px')
        element.style.setProperty('--upper-height', element.scrollHeight+'px')
        // Wait opening animation to end before scrolling into view
        element.addEventListener('animationend', function() {
            element.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start'});
        }, { once: true })
        element.classList.add('selected')
        element.classList.add('open')
    }
    
}   


// Create elements to show on the list side ====================================================================
function createListElement(feature, extraClass) {
    var listElement = document.createElement('button');
    listElement.id = feature.properties.location_id
    listElement.innerHTML = `
        <div class="horizontal-container even" style="padding-top: 2px; margin-top: 2px;">
            <h4>${feature.properties.name}</h4>
            <p>${feature.properties.address}</p>
        </div>
        <div id="info"><div>
            <div class="horizontal-container even">
                <h4>${feature.properties.email}</h4>
                <h4>${feature.properties.telephone}</h4>
                <button type="button" class="zoom_button" id="zoom_button"></button>
            </div>
            <div class="horizontal-container even">
                <h4>{{ _("description") }}</h4>
                <p>
                    "As a transportation entrepreneur, I take immense pride in the operations of my company. Our commitment to excellence shines through in every aspect of our business, from the reliability of our fleet to the professionalism of our drivers. We have cultivated a reputation for efficiency and timeliness, ensuring that our clients' goods reach their destinations safely and on schedule. What sets us apart is our unwavering dedication to customer satisfaction, always going above and beyond to meet their unique needs. With a focus on innovation and continuous improvement, we strive to exceed expectations, solidifying our position as a leader in the transportation industry."
                    - ChatGPT
                </p>
            </div>
            <div class="horizontal-container even">
                <h4>{{ _("services") }}</h4>
                <div style="justify-content: center">
                    <div id="services">
                                
                    </div>
                </div>
            </div>
        </div></div>
        <h4></h4>
        `;
    if (typeof extraClass !== 'undefined') {
        listElement.classList.add(extraClass)
    }
    var listDiv = document.getElementById('list_div')
    listElement.querySelector('#services').appendChild(createServiceElement(feature))
    listDiv.appendChild(listElement)
    listElement.classList.add('clickable_list_element');

    return listElement
} // ==============================================================================================
function addToListElement(element, feature) {
    console.log("Elementti "+feature.properties.address+" sisälsi jo yhden elementin")
    console.log(element.querySelector('#services'))
    element.querySelector('#services').appendChild(createServiceElement(feature))
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


//Returns a function which is to be used as 'pointToLayer' function in leaflet
function createMarker(feature, icon, L) {
    var [lat, lng] = feature.geometry.coordinates
    var marker = L.marker(L.latLng(lng, lat), { icon: icon })
    var popup = new L.popup({ autoClose: false, closeOnClick: false }).setContent(
        '<h4>' + feature.properties.name + '</h4><p>' + feature.properties.address+'</p>'
        )
    popup._initLayout()
    marker.i = feature.properties.location_id
    marker.bindPopup(popup);
    return marker;
}

export { createListElement, createMarker, runListElementAnimation, addToListElement }