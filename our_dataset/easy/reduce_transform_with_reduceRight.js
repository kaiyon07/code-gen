function reduceArray(nums, fn, init) {
    return nums.reverse().reduceRight((val, num) => fn(val, num), init);
  }