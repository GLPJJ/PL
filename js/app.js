/* 
    node.js 
    vscode 配置：
       {
            "name": "Node: Current File",
            "type": "node", //指定nodejs配置，参见node的安装
            "request": "launch",
            "program": "${file}"//指定运行当前文件
        }
*/

var a = 1;
var b = 2;

console.log('Manifest successfully generated' + (a + b));

