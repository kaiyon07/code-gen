var filter = function(arr, fn) {
    return arr.flatMap((i, j) => fn(i, j) ? [i] : []);
};