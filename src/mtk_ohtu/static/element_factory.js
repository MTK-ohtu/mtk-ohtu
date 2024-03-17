
var runListElementAnimation = function (element) {
    var minimum_height = element.querySelector('div').scrollHeight
    element.style.setProperty('--minimum-height', minimum_height+'px')
    element.style.setProperty('--total-height', (element.scrollHeight+20)+'px')
    if (element.classList.contains('open')) {
        element.classList.remove('selected')
        element.classList.remove('open')
        element.classList.add('closed')

    } else {
        element.classList.add('selected')
        // Wait opening animation to end before scrolling into view
        element.addEventListener('animationend', function() {
            element.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start'});
        }, { once: true })
        element.classList.remove('closed')
        element.classList.add('open')
    }
}

// Create elements to show on the list side ====================================================================
function createListElement(feature) {
    var listElement = document.createElement('button');
    listElement.id = feature.properties.address
    listElement.innerHTML = `
        <div class="horizontal-container even" style="padding-top: 2px; margin-top: 2px;">
            <h4>${feature.properties.name}</h4>
            <p>${feature.properties.address}</p>
            {%if show_route%}
                <div style="align-self: center; background-color: green; color: white; padding: 10px; margin-left: auto; text-align: center;">
                    CO2: {{emissions}} kg
                </div>
            {%endif%}
        </div>
        <div class="horizontal-container even" id="info">
            <p>
                
                "As a transportation entrepreneur, I take immense pride in the operations of my company. Our commitment to excellence shines through in every aspect of our business, from the reliability of our fleet to the professionalism of our drivers. We have cultivated a reputation for efficiency and timeliness, ensuring that our clients' goods reach their destinations safely and on schedule. What sets us apart is our unwavering dedication to customer satisfaction, always going above and beyond to meet their unique needs. With a focus on innovation and continuous improvement, we strive to exceed expectations, solidifying our position as a leader in the transportation industry."
                - ChatGPT
            </p>
            <button type="button" class="zoom_button" id="zoom_button"></button>
        </div>
        `;
    listElement.classList.add('clickable_list_element');
    var listDiv = document.getElementById('list_div')
    listDiv.appendChild(listElement)
    
    listElement.classList.add('open')
    runListElementAnimation(listElement)
    return listElement
} // ==============================================================================================

//Returns a function which is to be used as 'pointToLayer' function in leaflet
function createMarker(feature, icon, L) {
    var [lat, lng] = feature.geometry.coordinates
    var marker = L.marker(L.latLng(lng, lat), { icon: icon })
    marker.i = feature.properties.address
    marker.bindPopup('<h4>' + feature.properties.name + '</h4><p>' + feature.properties.address+'</p>', { autoClose: false});
    return marker;
}

export { createListElement, createMarker, runListElementAnimation }