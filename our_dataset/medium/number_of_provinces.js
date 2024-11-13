var findCircleNum = function (isConnected) {

    let provinces = 0;
    let visited = new Array(isConnected.length).fill(false);

    for (let i = 0; i < isConnected.length; i++) {
        if (!visited[i]) {
            provinces++;
            dfs(isConnected, visited, i);
        }
    }
    return provinces;
};

function dfs(isConnected, visited, i) {

    visited[i] = true;
    
    for (let j = 0; j < isConnected.length; j++) {
        if (isConnected[i][j] === 1 && !visited[j]) {
            dfs(isConnected, visited, j);
        }
    }
}