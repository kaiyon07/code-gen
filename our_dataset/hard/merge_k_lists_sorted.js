/**
 * @param {ListNode[]} lists
 * @return {ListNode}
 */

class ListNode {
  constructor(val, next) {
    this.val = (val === undefined ? 0 : val);
    this.next = (next === undefined ? null : next);
  }
}

function arrayToList(array) {
    if (array.length === 0) return null;

    let head = new ListNode(array[0]);
    let current = head;

    for (let i = 1; i < array.length; i++) {
        current.next = new ListNode(array[i]);
        current = current.next;
    }

    return head;
}

var mergeKLists = function (lists) {
    let nums = []

    for (let i = 0; i < lists.length; i++) {
        let current = lists[i]
        while (current !== null) {
            nums.push(current.val)
            current = current.next
        }
    }

    return arrayToList(nums.sort((a, b) => a - b))
};