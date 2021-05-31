/**
 * 
 * 开始新的JavaScript学习
 * 
 * 本篇内容：
 * 算术运算符
 * 比较运算符
 * 布尔运算符
 * 二进制位运算符
 * 其他运算符,运算顺序
 * 
 * 数据类型转换
 * 错误处理机制
 * console对象与控制台
 */

/*
加法运算符：x + y
减法运算符： x - y
乘法运算符： x * y
除法运算符：x / y
指数运算符：x ** y
余数运算符：x % y
自增运算符：++x 或者 x++
自减运算符：--x 或者 x--
数值运算符： +x
负数值运算符：-x
*/
console.log(true + true, 2 + false);
//除了加法运算符，其他算术运算符（比如减法、除法和乘法）都不会发生重载。
//它们的规则是：所有运算子一律转为数值，再进行相应的数学运算。
console.log("" + 2, false + "a", '3' + 4 + 5, 3 + 4 + "5");

/**
 * 如果运算子是对象，必须先转成原始类型的值，然后再相加
 * 
 * 对象转成原始类型的值，规则如下。
 * 首先，自动调用对象的valueOf方法.一般来说，对象的valueOf方法总是返回对象自身，
 * 再自动调用对象的toString方法，将其转为字符串
 */
var a = {};
console.log(a + 1);//[object Object]1
var b = {
    valueOf: function () {//重载valueOf方法
        return 2;
    }
};
console.log(b + 1);
//这里有一个特例，如果运算子是一个Date对象的实例，那么会优先执行toString方法
var c = new Date();
c.valueOf = function () { return 1 };
c.toString = function () { return 'hello' };

console.log(c + 2);// "hello2"

console.log("-1%2=", -1 % 2, "1%-2=", 1 % -2);//除余正负号由第一个数决定
var a = 0;
console.log(a++, ++a);

//数值运算符(+)的作用在于可以将任何值转为数值（与Number函数的作用相同）
console.log("一元操作符", +true, +[], +{});
//指数运算符是右结合，而不是左结合。即多个指数运算符连用时，先进行最右边的计算
console.log("指数运算", 2 ** 3 ** 2, (2 ** 3) ** 2);


/**
 * JavaScript 一共提供了8个比较运算符。
 * 
 * > 大于运算符
 * < 小于运算符
 * <= 小于或等于运算符
 * >= 大于或等于运算符
 * == 相等运算符
 * === 严格相等运算符
 * != 不相等运算符
 * !== 严格不相等运算符
 * 
 * 任何值（包括NaN本身）与NaN比较，返回的都是false
 * 
 * 如果运算子是对象，会转为原始类型的值，再进行比较。
 * 对象转换成原始类型的值，算法是先调用valueOf方法；如果返回的还是对象，再接着调用toString方法
 * 
 * undefined和null与其他类型的值比较时，结果都为false，它们互相比较时结果为true
 */
console.log(undefined === undefined, null === null, 'true' == true);//Number('true') == Number(true)

/**
 * 布尔运算符
 * 
 * 取反运算符：!
 * 且运算符：&&
 * 或运算符：||
 * 三元运算符：?:
 * 
 * 三元条件运算符（?:）
 */

/**
 * 二进制位运算符
 * 
 * 二进制或运算符（or）：符号为|，表示若两个二进制位都为0，则结果为0，否则为1。
 * 二进制与运算符（and）：符号为&，表示若两个二进制位都为1，则结果为1，否则为0。
 * 二进制否运算符（not）：符号为~，表示对一个二进制位取反。
 * 异或运算符（xor）：符号为^，表示若两个二进制位不相同，则结果为1，否则为0。
 * 左移运算符（left shift）：符号为<<
 * 右移运算符（right shift）：符号为>>
 * 带符号位的右移运算符（zero filled right shift）：符号为>>>
 */
console.log("1 | 0, 1 & 0, ~1, 1 ^ 0 =", 1 | 0, 1 & 0, ~1, 1 ^ 0)
console.log("1<<2,512>>2 =", 1 << 2, 512 >> 2)

//“>>>”运算符执行五符号右移位运算。它把无符号的 32 位整数所有数位整体右移。
//对于无符号数或正数右移运算，无符号右移与有符号右移运算的结果是相同的。
//对于负数来说，无符号右移将使用 0 来填充所有的空位，同时会把负数作为正数来处理，
//所得结果会非常大所以，使用无符号右移运算符时要特别小心，避免意外错误。
//计算机使用补码来表示负数，所以负数很大。
console.log("-1000 >> 1, -1000 >>> 1 =", -1000 >> 1, -1000 >>> 1)
debugger
/**
 * void 运算符
 * 逗号运算符
 * 
 * 记住所有运算符的优先级，是非常难的，也是没有必要的
 * 圆括号的作用(优先级最高)
 * 左结合与右结合
 */

console.log(void (0));


/**
 * 强制转换主要指使用Number()、String()和Boolean()三个函数
 * 
 * 简单的规则是，Number方法的参数是对象时，将返回NaN，除非是包含单个数值的数组
 * 
 *  第一步，调用对象自身的valueOf方法。如果返回原始类型的值，则直接对该值使用Number函数，不再进行后续步骤。
 *  第二步，如果valueOf方法返回的还是对象，则改为调用对象自身的toString方法。
 *      如果toString方法返回原始类型的值，则对该值使用Number函数，不再进行后续步骤。
 *  第三步，如果toString方法返回的是对象，就报错
 */

/*
Number转换规则
*/
var obj = { x: 1 };
console.log("Number(obj)=", Number(obj)); // NaN

// 等同于
if (typeof obj.valueOf() === 'object') {
    Number(obj.toString());
} else {
    Number(obj.valueOf());
}

/**
 * 
 * String方法背后的转换规则，与Number方法基本相同，只是互换了valueOf方法和toString方法的执行顺序。
 * 
 *  先调用对象自身的toString方法。如果返回原始类型的值，则对该值使用String函数，不再进行以下步骤。
 *  如果toString方法返回的是对象，再调用原对象的valueOf方法。如果valueOf方法返回原始类型的值，
 *      则对该值使用String函数，不再进行以下步骤。
 *  如果valueOf方法返回的是对象，就报错。
 */

console.log(String({ a: 1 }), String({ a: 1 }.toString()));

/**
 * Boolean函数可以将任意类型的值转为布尔值。
 */

/*
它的转换规则相对简单：除了以下五个值的转换结果为false，其他的值全部为true。

undefined
null
-0或+0
NaN
''（空字符串）
*/

/**
 * 自动转换
 * 
 * 第一种情况，不同类型的数据互相运算
 * 第二种情况，对非布尔值类型的数据求布尔值
 * 第三种情况，对非数值类型的值使用一元运算符（即+和-）
 * 
 * 自动转换为布尔值
 * 自动转换为字符串
 * 自动转换为数值
 */

/**
 * 错误处理机制
 * 
 * Error
 * message：错误提示信息
 * name：错误名称（非标准属性）
 * stack：错误的堆栈（非标准属性）
 */
var err = new Error('出错了');
console.log("错误实例 =", err.message, err.name, err.stack) // "出错了"

/**
 * SyntaxError对象是解析代码时发生的语法错误
 * ReferenceError对象是引用一个不存在的变量时发生的错误
 * RangeError对象是一个值超出有效范围时发生的错误。
 *      主要有几种情况，一是数组长度为负数，二是Number对象的方法参数超出范围，以及函数堆栈超过最大值
 * TypeError对象是变量或参数不是预期类型时发生的错误
 * URIError对象是 URI 相关函数的参数不正确时抛出的错误，
 *      主要涉及encodeURI()、decodeURI()、encodeURIComponent()、decodeURIComponent()、escape()和unescape()这六个函数
 * eval函数没有被正确执行时，会抛出EvalError错误。该错误类型已经不再使用了，只是为了保证与以前代码兼容，才继续保留。
 */

/**
 * 自定义错误
 */
function UserError(message) {
    this.message = message || '默认信息';
    this.name = 'UserError';
}

UserError.prototype = new Error();
UserError.prototype.constructor = UserError;
//上面代码自定义一个错误对象UserError，让它继承Error对象。然后，就可以生成这种自定义类型的错误了

/**
 * throw 语句
 * throw语句的作用是手动中断程序执行，抛出一个错误
 * 
 * 
 * try...catch 结构
 */

try {
    console.log("抛出异常");
    throw new UserError("自定义错误");
} catch (error) {
    console.log("error=", error);
} finally {
    console.log("finally");
}

/**
 * try代码块没有发生错误，而且里面还包括return语句，但是finally代码块依然会执行。
 * 注意，只有在其执行完毕后，才会显示return语句的值
 * return语句的执行是排在finally代码之前，只是等finally代码执行完毕后才返回。
 */
var count = 0;
function countUp() {
    try {
        return count;//即使有return,finally还会执行
    } finally {
        count++;
    }
}

console.log("countUp()=", countUp());
console.log("count=", count);

//再看下面的例子
function f() {
    try {
        console.log(0);
        throw 'bug';
        console.log(1);
    } catch (e) {
        console.log(2);
        return true; // 这句原本会延迟到 finally 代码块结束再执行
        console.log(3); // 不会运行
    } finally {
        console.log(4);
        return false; // 这句会覆盖掉前面那句 return
        console.log(5); // 不会运行
    }

    console.log(6); // 不会运行
}

var result = f();
console.log("result=", result);

function f1() {
    try {
        console.log('f1 出错了！');
        throw '出错了！';
    } catch (e) {
        console.log('f1 捕捉到内部错误');
        throw e; // 这句原本会等到finally结束再执行
    } finally {
        console.log('f1 finally');
        return false; // 直接返回,导致无法抛出异常
    }
}

try {
    f1();
} catch (e) {
    // 此处不会执行
    console.log('f1 caught outer "bogus"');
}
console.log("\n");

/**
 * console对象
 * 
 * console.log方法支持以下占位符，不同类型的数据必须使用对应的占位符。

%s 字符串
%d 整数
%i 整数
%f 浮点数
%o 对象的链接
%c CSS 格式字符串
 */
console.log('console格式字符串 %s + %s ', 1, 1, '= 2');

/**
 * 类似的打印函数还有
 * console.info
 * console.debug
 * 
 * console.warn()
 * console.error()
 * 
 * 
 * 可以这样理解：
 * log方法是写入标准输出（stdout），warn方法和error方法是写入标准错误（stderr）。
 */
console.info("console.info");
//默认情况下，console.debug输出的信息不会显示，只有在打开显示级别在verbose的情况下，才会显示。
console.debug("console.debug");

console.warn("console.warn");
console.error("console.error");

var obj = {
    a: 1,
    b: 2
};
console.table(obj);//仅针对浏览器环境，node环境没有输出

//count方法用于计数，输出它被调用了多少次。
//该方法可以接受一个字符串作为参数，作为标签，对执行次数进行分类
// console.count();

function greet(user) {
    console.count(user);//node环境 莫名其妙打印了两次
    console.log('hi ' + user);
}
greet('bob');
greet('alice');
greet('bob');

console.log(obj);
console.dir(obj);//node环境 跟log输出一致
// console.dir(obj, { colors: true });
//dirxml方法主要用于以目录树的形式，显示 DOM 节点
console.dirxml(obj);//node环境 无输出

//断言的用法
// console.assert(false, '判断条件不成立');

//这两个方法用于计时，可以算出一个操作所花费的准确时间
console.time("Test Time");
console.timeEnd("Test Time");//node环境 会打出两个时间。。。

//将显示的信息分组。它只在输出大量信息时有用，分在一组的信息，可以用鼠标折叠/展开。
console.group('一级分组');
console.log('一级分组的内容');

console.group('二级分组');
console.log('二级分组的内容');

console.groupEnd(); // 二级分组结束
console.groupEnd(); // 一级分组结束
//console.groupCollapsed方法与console.group方法很类似

//打印调用堆栈
console.log(typeof console.trace());
//清空打印信息
console.clear();//node vscode 环境没用

/**
 * 控制台命令行 API
 * 
 * $_属性返回上一个表达式的值
 * 
 * $0 - $4 
 * 控制台保存了最近5个在 Elements 面板选中的 DOM 元素，$0代表倒数第一个（最近一个），
 * $1代表倒数第二个，以此类推直到$4
 * 
 * $(selector)返回第一个匹配的元素，等同于document.querySelector()
 * 注意，如果页面脚本对$有定义，则会覆盖原始的定义。比如，页面里面有 jQuery，
 * 控制台执行$(selector)就会采用 jQuery 的实现，返回一个数组
 * 
 * $$(selector)返回选中的 DOM 对象，等同于document.querySelectorAll
 * 
 * $x(path)方法返回一个数组，包含匹配特定 XPath 表达式的所有 DOM 元素
 * 
 * inspect(object)方法打开相关面板，并选中相应的元素，显示它的细节
 * 
 * getEventListeners(object)方法返回一个对象，该对象的成员为object登记了回调函数的各种事件
 * （比如click或keydown），每个事件对应一个数组，数组的成员为该事件的回调函数
 * 
 * keys(object)方法返回一个数组，包含object的所有键名。
 * 
 * values(object)方法返回一个数组，包含object的所有键值
 * 
 * monitorEvents(object[, events])方法监听特定对象上发生的特定事件
 * 事件发生时，会返回一个Event对象，包含该事件的相关信息。unmonitorEvents方法用于停止监听。
 * 
 * 命令行 API 还提供以下方法。
 * 
 * clear()：清除控制台的历史。
 * copy(object)：复制特定 DOM 元素到剪贴板
 * dir(object)：显示特定对象的所有属性，是console.dir方法的别名
 * dirxml(object)：显示特定对象的 XML 形式，是console.dirxml方法的别名。
 */

/**
 * debugger语句主要用于除错，作用是设置断点。如果有正在运行的除错工具，
 * 程序运行到debugger语句时会自动停下。如果没有除错工具，debugger语句不会产生任何结果，
 * JavaScript 引擎自动跳过这一句。
 */
// debugger//程序运行到这里自动停住

