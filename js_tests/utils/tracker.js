function Tracker() {
    this.calls = Array();
}


Tracker.prototype.called = function() {
    return this.calls.length;
}


Tracker.prototype.calledWith = function() {
    this.calls.push(Array.prototype.slice.call(arguments, 0));
}
