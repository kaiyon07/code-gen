var predictPartyVictory = function(senate) {
    senate = senate.split('');
    while(senate.length) {
        var first = senate.shift();
        var len = senate.length;

        for(var i=0; i<len; i++) {
            if(first != senate[i]) {
                senate.splice(i, 1);
                senate.push(first);
                break;
            }
        }
        if(i == len) {
            return first == 'D' ? 'Dire' : 'Radiant';
        }
    }
};