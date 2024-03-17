// Leaflet marker icons
var okTruck = new L.Icon({
    iconUrl: '/static/images/ok_truck.png',
    shadowUrl: '/static/images/point.png',
    iconSize: [25, 25],
    iconAnchor: [8, 25],
    popupAnchor: [1, -34],
    shadowSize: [10, 10],
    shadowAnchor: [0, 0]
});

var badTruck = new L.Icon({
    iconUrl: '/static/images/bad_truck.png',
    shadowUrl: '/static/images/point.png',
    iconSize: [25, 25],
    iconAnchor: [8, 25],
    popupAnchor: [1, -34],
    shadowSize: [10, 10],
    shadowAnchor: [0, 0]
});

var goal = new L.Icon({
    iconUrl: '/static/images/goal_button.png',
    shadowUrl: '/static/images/point.png',
    iconSize: [35, 35],
    iconAnchor: [0, 35],
    popupAnchor: [1, -34],
    shadowSize: [10, 10],
    shadowAnchor: [0, 5]
});

var product = new L.Icon({
    iconUrl: '/static/images/product_icon.png',
    iconSize: [35, 35],
    iconAnchor: [17,35],
    popupAnchor: [1, -34],
});

export { okTruck, badTruck, goal, product }