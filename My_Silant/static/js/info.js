function setOrder_by(name) {
window.sessionStorage.setItem('order_by', name);
reload();
}
function setFilter_te(name) {
window.sessionStorage.setItem('te', "&te=" + name);
reload();
}
function reload() {
//    sessionStorage.clear();
    console.log('reload стартовал');
    console.log('sessionStorage order_by = ', window.sessionStorage.getItem('order_by'));
    if (window.sessionStorage.getItem('order_by') === null) {
        order_by = "?order_by=date_of_shipment_from_the_factory";
    }
    console.log('order_by2 = ', order_by);
    httpParam = order_by + window.sessionStorage.getItem('te');
    console.log('httpParam = ', httpParam);
    window.location.href = httpParam;

}