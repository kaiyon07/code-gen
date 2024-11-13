var filter = function(arr, fn) {
    const result = [];
    arr.forEach((value, index) => {
      if (fn(value, index)) {
        result.push(value);
      }
    });
    return result;
  };