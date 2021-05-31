// In Node.js
//设置npm下载镜像。
//npm config set registry https://registry.npm.taobao.org 
//查看npm查找路径
//npm prefix -g
//从cmd中进入node 查看node require查找路径 module.paths
//这个一般是安装在用户目录下/node_modules
//npm install web3

const Web3 = require('web3');

let web3 = new Web3('ws://localhost:8546');
console.log(web3);
