function reduceArray(nums, fn, init) {
    if (nums.length === 0) {
      return init;
    } else {
      const head = nums[0];
      const tail = nums.slice(1);
      const val = fn(init, head);
      return reduceArray4(tail, fn, val);
    }
  }