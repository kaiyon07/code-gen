/**
 * @param {string} s
 * @return {string}
 */
var removeStars = function(s) {
    let i = 0;
        let stk = [];
         while(i<s.length){
             if(s.charAt(i)==="*"){
                if(stk.length>0){
                    stk.pop();
                }
             }
             else {
                 stk.push(s.charAt(i))
             }
             i++;
         }
        return stk.join("");
    };