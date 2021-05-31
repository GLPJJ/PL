function Func1() {
    console.log("Func1 before");

    setTimeout(function () {
        console.log("Func1 do...");
    }, 1000)

    console.log("Func1 after");
}
// Func1();
/** 
 * 在学习今天的知识之前看上面的普通代码。
 * 
 * 上面依次打印:
 *      Func1 before
 *      Func1 after
 *      Func1 do...
 * 
 * 很多的异步操作基本都是这样执行的，所以我们需要添加各种各样的回调机制来等待处理完成才能后续操作
 * 但是过多的监听导致我们的代码显的复杂，看下面的例子
*/
function Func2() {
    console.log("Func2 before");

    var after = function () {
        console.log("Func2 after");
    }
    setTimeout(function () {
        console.log("Func2 do...");
        after();
    }, 1000)
}
// Func2();
/**
 * 上面的代码就是通过设定一个回调函数 after 来保证我们的任务执行顺序，这个例子比较简单，但是如果项目比较复杂
 * 越来越多的after 会让你受不了。。。
 * 
 * 新的ES6标准提供了Promise await async 关键字，看下面的例子
 */
async function Func3() {
    console.log("Func3 before");
    await //这里如果没有await，那么程序将直接运行到 after,我们的Promise对象的方法也会执行，但是毫无意义
        new Promise(function (resolve, reject) {
            setTimeout(function () {
                console.log("Func3 do...");
                resolve();
            }, 1000)
        });
    console.log("Func3 after");
}
// Func3();
/**
 * async 声明表示这是一个异步函数，因为我们在里面有使用await操作，所以必须申明，否则将报错
 * await 表示我们将等待一个结果，这个结果由Promise对象提供，它只提供一个resolve函数和reject函数，
 * await默认等待一个resolve结果，如果先收到reject，则将throw异常
 */

//更多尝试
async function Func4(val) {
    console.log("Func4 before");
    var newVal1 = await 1;//这里自动转换成Promise对象，并将表达式结果返回
    console.log("Func4 newVal1=", newVal1);
    /**
     * 先resolve,后reject测试
     */
    var newVal2 = await new Promise(function (resolve, reject) {
        setTimeout(function () {
            resolve(val + 10);
            console.log("Func4 timeout 1", val);
        }, 2000)

        setTimeout(function () {
            reject(val + 20);
            console.log("Func4 timeout 2", val);
        }, 3000)
    })

    newVal1 += newVal2;
    console.log("Func4 after", newVal1, newVal2);

    // 先reject,后resolve测试
    var newVal3 = await new Promise(function (resolve, reject) {
        setTimeout(function () {
            resolve(val + 10)
            console.log("Func4 timeout 3", val);
        }, 2000)

        setTimeout(function () {
            reject(val + 20)
            console.log("Func4 timeout 4", val);
        }, 1000)
    }).then(function (value) {
        //由于上面reject我们没有捕获，我们这里将不能执行到
        console.log("Func4 after 2", value, newVal3);
    }).catch(function (reason) {
        console.log("Func4 error " + reason);
    });

    //上面的测试表面，await只接受第一个处理的结果，不管是resolve或是reject
    //如果可能出现reject的结果，那么我们最好处理逻辑代码写在then和catch里面

    //或者对整个Promise对象进行 try...catch
}

console.log("call Func4 1");
Func4(10).then(function(){
    console.log("call Func4 3");
});
//这里的代码会直接跟着执行。。。
console.log("call Func4 2");
