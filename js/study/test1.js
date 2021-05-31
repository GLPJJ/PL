/**
 * vs code 配置
{
            "type": "node",
            "request": "launch",
            "name": "Node: 当前文件",
            "program": "${file}",
            "console": "integratedTerminal"
}
 * 
 * 开始新的JavaScript学习
 * 
 * 本篇内容：
 * 概述
 * null,undefined和boolean
 * 数值
 * 字符串
 * 对象
 * 函数
 * 数组

 URL Encode
 encodeURI 编解码
 Base64 编解码
 */

/* 变量提升
 *  JavaScript 引擎的工作方式是，先解析代码，获取所有被声明的变量，然后再一行一行地运行。
 *  这造成的结果，就是所有的变量的声明语句，都会被提升到代码的头部，这就叫做变量提升（hoisting）。
 */
console.log(a);//这里变量提升
var a = 1;
console.log(a);

/**
 * 变量提升
 * 上面的代码等价于:
 * var a;
 * console.log(a);
 * a = 1;
 * console.log(a);
 * 
 */

/**
 * 标识符
 * 
 * 第一个字符，可以是任意 Unicode 字母（包括英文字母和其他语言的字母），以及美元符号（$）和下划线（_）。
 * 第二个字符及后面的字符，除了 Unicode 字母、美元符号和下划线，还可以用数字0-9
 */

var 临时变量 = 1;
console.log("临时变量=" + 临时变量);

{
  var b = 2;//ES5 JavaScript 的区块不构成单独的作用域（scope）
}
console.warn(b);//这里也能访问b

switch (a) {//switch使用的是严格相等运算符 ===
  case true:
    console.log("发生类型转换");
    break;
  default:
    console.log("没有发生类型转换")
}

/**
 * js标签
 */
run: {
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      console.log("i = ");
      if (i === 1 && j === 1)
        break run;//break 搭配标签，跳出双层循环，continue也可以搭配标签
      console.log(i + ";" + j);
    }
  }
}

/**
 * JavaScript 有三种方法，可以确定一个值到底是什么类型。
 * typeof运算符
 * instanceof运算符
 * Object.prototype.toString方法
 */
console.log("类型判断:");
console.log("typeof a=" + typeof a);
console.log("typeof ''=" + typeof "");
console.log("typeof true=" + typeof true);
var f = function () { }
console.log("typeof f=" + typeof f);
console.log("typeof undefined=" + typeof undefined);
/**
 * null的类型是object，这是由于历史原因造成的。
 * 1995年的 JavaScript 语言第一版，只设计了五种数据类型（对象、整数、浮点数、字符串和布尔值），
 * 没考虑null，只把它当作object的一种特殊值。后来null独立出来，作为一种单独的数据类型，
 * 为了兼容以前的代码，typeof null返回object就没法改变了。
 */
console.log("typeof null=" + typeof null);
console.log("typeof window=" + typeof window);

var arra = [];
console.log("typeof arra=" + typeof arra);
console.log("typeof {}=" + typeof {});
console.log("\n");
/*
判断一个值是否定义
// 错误的写法
if (v) {
  // ...
}
// ReferenceError: v is not defined

// 正确的写法
if (typeof v === "undefined") {
  // ...
}
*/

// instanceof 运算等级低
console.log("arra instanceof Array=" + (arra instanceof Array));
console.log(Object.prototype.toString.call(a));

console.log("undefined == null = " + (undefined == null));//这里不是严格相等
console.log("Number(null)=" + Number(null));//null依据c++的标准，自动转0
console.log("a + null = " + (a + null));

console.log("Number(undefined)=" + Number(undefined)) // NaN
console.log(5 + undefined) // NaN
console.log("\n");
/**
 * 转换规则是除了下面六个值被转为false，其他值都视为true
 * 
 * undefined
 * null
 * false
 * 0
 * NaN
 * ""或''（空字符串）
 */
console.log(!!"");

/**
 * JavaScript 内部，所有数字都是以64位浮点数形式储存，即使整数也是如此。
 * 所以，1与1.0是相同的，是同一个数
 */
console.log("1 === 1.0=" + (1 === 1.0));
var _3 = 0.1 + 0.2; //0.30000000000000004 浮点数计算有误差
var __3 = 0.01 + 0.02;
var __2 = 0.01 + 0.01;//0.02
var __1 = 0.01
console.log("0.1+0.2 === 0.3=" + (_3 == 0.3) + ",__2=" + (__2 == 0.02) + ",__3=" + (__3 == 0.03));
console.log("(0.01)10 = (" + __1 + ")2\n");
/**
 * js 数值表示 DOUBLE、FLOAT64
 * 第1位：符号位，0表示正数，1表示负数
 * 第2位到第12位（共11位）：指数部分
 * 第13位到第64位（共52位）：小数部分（即有效数字）
 * 
 * 数值表达式： (-1)^符号位 * 1.xx...xx * 2^指数部分
 * 
 * IEEE 754 规定，如果指数部分的值在0到2047之间（不含两个端点），
 * 那么有效数字的第一位默认总是1，不保存在64位浮点数之中
 * 
 * 所以有效数字是 (正/负)1*1.(52位) * 2^(指数为1)
 * [-2^53 , 2^53] 有效数字表示范围，
 * 
 * 指数部分的表示范围是 -1023(开区间) ~0~ 1023 (2047各分一半) 
 * (正/负)* 0.(2^-52) * 2^-1023  小数部分最小取到 2^-52次幂
 * (正/负)* 1.99999 * 2^1023     小数部分最大取到 1.999999 < 2
 * (-2^1024,-2^-1075] and [2^-1075 , 2^1024) 
 * 
 * 顺便说一下单精度FLOAT32 
 * 1符号位
 * 第2~9位（共8位）:指数部分
 * 第10~32位（共23位）:小数部分
 * 
十进制转二进制
小数分为整数部分和小数部分，整数部分的转换照常进行，不断的除2得到，小数部分刚好是不断的乘2得到，一直到小数部分为0，或者已经达到了对应的精度，以69.3125为例。
69.3125
整数部分：69 = 64 + 4 + 1 = 2^6 + 2^2 + 2^0
对应的二进制数为：0100 0101
小数部分：转换过程如下 -> 不断乘2，取出结果中的整数部分
0.3125*2 = 0.625  ---->整数位 0
0.625*2  = 1.25   ---->整数位 1
0.25*2   = 0.5    ---->整数位 0
0.50*2   = 1.0    ---->整数位 1
对应的二进制数为：0101
 */
console.log("数值精度测试");
console.log(Math.pow(2, 53));
console.log(Math.pow(2, 53) + 1);//超出有效数字范围，精度无法保证
console.log(Math.pow(-2, 53));
console.log(Math.pow(-2, 53) - 1);//超出有效数字范围，精度无法保证
console.log("\n");

console.log("数值范围测试");
console.log(Math.pow(2, 1023)); //
console.log(Math.pow(2, 1024)); // Infinity 正向溢出
console.log(Math.pow(2, -1075)); // 0
console.log(Math.pow(2, -1076)); // 0 负向溢出
console.log('Number.MAX_VALUE=' + Number.MAX_VALUE + ";Number.MIN_VALUE=" + Number.MIN_VALUE);
console.log("\n");
/**
 * 科学计数
 * JavaScript 的数值有多种表示方法，可以用字面形式直接表示，比如35（十进制）和0xFF（十六进制）。
 * 数值也可以采用科学计数法表示
 * 
 * JS自动将数字转成科学计数的规则：
 *  小数点前的数字多于21位
 *  小数点后的零多于5个
 */
console.log("科学计数 123e3=" + 123e3); // 123000
console.log("科学计数 123e-3" + 123e-3); // 0.123
console.log("科学计数 -3.1E+12=" + -3.1E+12);
console.log("科学计数 .1e-23=" + .1e-23);
console.log("自动转科学计数小数点前的数字多于21个", 123456789012345678901, 1234567890123456789012);
console.log("自动转科学计数小数点后的零多于5个", 0.000001, 0.0000001, 0.0000011);

console.log("二进制 (0b/0B)110=" + 0b110);
console.log("八进制 (0o/0O)110=" + 0o110);
console.log("十六进制 (0x/0X)110=" + 0x110);
console.log("\n");
/**
 * 几个特殊的数值: 负0,NaN,Infinity
 */

/**
 * 正负0 默认情况都是当做0，除非作为分母的时候，得到Infinity和-Infinity
 */
console.log("正负0", "+0 === -0 : ", (+0 === -0), (+0).toString());
console.log("正负0", "0 === -0 : ", (0 === -0), (-0).toString());
console.log("正负0", 1 * +0, 1 / +0);
console.log("正负0", 1 * -0, 1 / -0);
console.log("正负0", 1 * +0 === 1 * -0, 1 / 0 === 1 / +0, 1 / +0 === 1 / -0);
console.log("\n");

/**
 * NaN不等于任何值，包括它本身。
 * NaN与任何数（包括它自己）的运算，得到的都是NaN
 */
var 万村 = 2;
console.log("NaN(Not a Number)", 2 + 万村, 2 - "万村2", Math.acos(2), 0 / 0, typeof NaN);
console.log("NaN == NaN", NaN == NaN, Boolean(NaN));
console.log("\n");

/**
 * Infinity(正无穷)大于一切数值（除了NaN），-Infinity(负无穷)小于一切数值（除了NaN）。
 * Infinity和NaN比较都返回false
 * 
 * Infinity的四则运算，符合无穷的数学计算规则。
 * Infinity与null计算时，null会转成0，等同于与0的计算
 * Infinity与undefined计算，返回的都是NaN
 */
console.log("Infinity > 1000", Infinity > 1000);
console.log("-Infinity < -1000", -Infinity < -1000);
console.log(Infinity > NaN, Infinity <= NaN)
console.log(5 * Infinity, 5 - Infinity, Infinity / 5, 5 / Infinity);
console.log(0 * Infinity, 0 / Infinity, Infinity / 0);
console.log(Infinity * Infinity, Infinity + Infinity, Infinity / Infinity, Infinity - Infinity);
console.log(null * Infinity, null / Infinity, Infinity / null);
console.log("\n");
/**
 * parseInt方法用于将字符串转为整数
 * 如果字符串头部有空格，空格会被自动去除
 * 如果parseInt的参数不是字符串，则会先转为字符串再转换
 * 字符串转为整数的时候，是一个个字符依次转换，如果遇到不能转为数字的字符，就不再进行下去，返回已经转好的部分
 * 如果字符串的第一个字符不能转化为数字（后面跟着数字的正负号除外），返回NaN
 * 如果字符串以0x或0X开头，parseInt会将其按照十六进制数解析；如果字符串以0开头，将其按照10进制解析
 */
console.log("parseInt", parseInt('0x10'), parseInt(1.9), parseInt(1.4), parseInt(""), parseInt('\t\v\r12.34\n '));
//对于那些会自动转为科学计数法的数字，parseInt会将科学计数法的表示方法视为字符串，因此导致一些奇怪的结果。
console.log("parseInt(1000000000000000000000.5)", parseInt(10000000000000000000.5), parseInt(1000000000000000000000.5));
console.log("parseInt(0.0000008)", parseInt(0.000008), parseInt(0.0000008));
/**
 * parseInt方法还可以接受第二个参数（2到36之间）
 * 如果第二个参数不是数值，会被自动转为一个整数。
 * 这个整数只有在2到36之间，才能得到有意义的结果，超出这个范围，则返回NaN。
 * 如果第二个参数是0、undefined和null，则直接忽略
 */
console.log(parseInt('10', 37), parseInt('10', 1), parseInt('10', 0), parseInt('10', null), parseInt('10', undefined));

/**
 * parseFloat与parseInt类似，科学计数得以正确转换
 */
console.log("parseFloat和Number", parseFloat(true), Number(true), parseFloat('\t\v\r12.34\n '));
console.log("parseFloat和Number", parseFloat(null), Number(null));
console.log("parseFloat和Number", parseFloat(''), Number(''));
console.log("parseFloat和Number", parseFloat('123.45#'), Number('123.45#'));
console.log("\n");
/**
 * 但是，isNaN只对数值有效，如果传入其他值，会被先转成数值(Number函数)。
 * 比如，传入字符串的时候，字符串会被先转成NaN，所以最后返回true，这一点要特别引起注意。
 * 也就是说，isNaN为true的值，有可能不是NaN，而是一个字符串
 */
console.log("isNaN", isNaN(true), isNaN(NaN), isNaN("abc"));
//但是，对于空数组和只有一个数值成员的数组，isNaN返回false,原因是这些数组能被Number函数转成数值
console.log("isNaN", isNaN({}), isNaN([]), isNaN(["abc"]), isNaN([233]));
//判断NaN更可靠的方法是，利用NaN为唯一不等于自身的值的这个特点，进行判断
function myIsNaN(value) {
  return value !== value;
}
console.log("myIsNan", myIsNaN("a"), myIsNaN(NaN));

/**
 * isFinite()
 * isFinite方法返回一个布尔值，表示某个值是否为正常的数值
 */
console.log("isFinite", isFinite(2), isFinite(Infinity), isFinite(NaN), isFinite(null));
console.log("\n");
/**
 * 字符串：字符串就是零个或多个排在一起的字符，放在单引号或双引号之中
 * 
 * \0 ：null（\u0000）
 * \b ：后退键（\u0008）
 * \f ：换页符（\u000C）
 *  \n ：换行符（\u000A）
 * \r ：回车键（\u000D）
 * \t ：制表符（\u0009）
 * \v ：垂直制表符（\u000B）
 * \' ：单引号（\u0027）
 * \" ：双引号（\u0022）
 * \\ ：反斜杠（\u005C）
 * 
 * 反斜杠还有三种特殊用法 
 *  反斜杠后面紧跟三个八进制数（000到377），代表一个字符
 *  \x后面紧跟两个十六进制数（00到FF），代表一个字符
 *  \u后面紧跟四个十六进制数（0000到FFFF），代表一个字符
 * 
 * 如果在非特殊字符前面使用反斜杠，则反斜杠会被省略
 * 如果字符串的正常内容之中，需要包含反斜杠，则反斜杠前面需要再加一个反斜杠，用来对自身转义
 */
console.log("字符串", '\2511', '\xA91', '\u00A91', "\a", "\\");

/**
 * 字符串可以被视为字符数组，因此可以使用数组的方括号运算符，用来返回某个位置的字符（位置编号从0开始）
 * 但是字符串是只读的，所有的更改都无效
 * 
 * length属性也是只读的
 */
var s = "hello";
delete s[0];
s[1] = "2";
s.length = 10;
console.log("字符串s", s, s[0], s[100], s.length);

/**
 * 解析代码的时候，JavaScript 会自动识别一个字符是字面形式表示，还是 Unicode 形式表示。
 * 输出给用户的时候，所有字符都会转成字面形式
 */
var f\u006F\u006F = 'abc';//代表foo，很少这样写，增加阅读代码难度。。。
console.log("foo=", foo);

/**
 * 总结一下，对于码点在U+10000到U+10FFFF之间的字符，JavaScript 总是认为它们是两个字符（length属性为2）。
 * 所以处理的时候，必须把这一点考虑在内，也就是说，JavaScript 返回的字符串长度可能是不正确的
 */
console.log("'𝌆'.length", '𝌆'.length);//其实是1个字符
console.log("\n");
/**
 * Base64 转码
 * 所谓 Base64 就是一种编码方法，可以将任意值转成 0～9、A～Z、a-z、+和/这64个字符组成的可打印字符。
 * 使用它的主要目的，不是为了加密，而是为了不出现特殊字符，简化程序的处理。
 * JavaScript 原生提供两个 Base64 相关的方法。
 * 
 * 只存在于浏览器，nodejs中不含下面的两个方法，
 * btoa()：任意值转为 Base64 编码
 * atob()：Base64 编码转为原来的值
 */

if (typeof btoa === "function") {
  /** 浏览器环境 */
  var strBase64 = btoa("Hello World!");
  console.log("Base64 浏览器环境", strBase64, atob(strBase64));

  //将非 ASCII 码的字符转换成Base64编码
  function b64Encode(str) {
    return btoa(encodeURIComponent(str));
  }

  function b64Decode(str) {
    return decodeURIComponent(atob(str));
  }

  b64Encode('你好') // "JUU0JUJEJUEwJUU1JUE1JUJE"
  b64Decode('JUU0JUJEJUEwJUU1JUE1JUJE') // "你好"
} else {
  /** Node环境 */
  var strBase64 = new Buffer('Hello World! 我').toString('base64');
  console.log("Base64 Node环境", strBase64, new Buffer(strBase64, 'base64').toString());
}
console.log("\n");
/**
 * 对象： 对象就是一组“键值对”（key-value）的集合，是一种无序的复合数据集合
 * 对象的所有键名都是字符串（ES6 又引入了 Symbol 值也可以作为键名），所以加不加引号都可以。
 * 如果键名是数值，会被自动转为字符串
 * 
 * 如果键名不符合标识名的条件（比如第一个字符为数字，或者含有空格或运算符），且也不是数字，则必须加上引号，否则会报错。
 * 
 * // 报错
 * var obj = {
 * 1p: 'Hello World'
 * };
 */
var obj = {
  1: 'a',       //"1": "a",
  3.2: 'b',     //"3.2": "b",
  1e2: true,    //"100": true,
  1e-2: true,   //"0.01": true,
  .234: true,   //"0.234": true,
  0xFF: true    //"255": true  String(0xFF)
};
console.log('obj["100"]=', obj["100"], obj[100], String(0xFF));

/**
 * 对象的方法
 * var obj={p:function(){}}
 * 链式应用
 * var obj={p:{q:0}}
 * 动态创建
 * var obj = {};obj.r = 2;
 * 
 * 对象的引用
 * 如果不同的变量名指向同一个对象，那么它们都是这个对象的引用，也就是说指向同一个内存地址。
 * 修改其中一个变量，会影响到其他所有变量
 * 两个变量都指向原始类型的值，则更改其中一个不会影响到第二个
 */


console.log("行首是大括号的情况：")
console.log(eval("{foo: 123}"));//这里被当成了表达式，代码库理解
console.log(eval("({foo: 123})"));//这里加圆括号当成是一个对象
console.log("\n");
/**
 * 对象属性的读取使用 . 和 []
 * []中必须是字符串，否则会当成变量处理
 * 数值键名不能使用点运算符 obj.123 不允许
 * 
 * 赋值也可以使用 . 和 []
 */


/**
 * 属性的查看
 */
console.log("查看一个对象本身的所有属性 1", Object.keys(obj));
/**
 * 属性的删除
 * 即使对象obj没有100的属性，delete也会返回true,
 * 只有一种情况，delete命令会返回false，那就是该属性存在，且不得删除
 */
delete obj["100"];//返回true
console.log("删除后，查看一个对象本身的所有属性 2", Object.keys(obj));
var obj1 = Object.defineProperty({}, 'p', {
  value: 123,
  configurable: false
});
console.log("obj1.p:", obj1.p); // 123
console.log("delete obj1.p:", delete obj1.p); // false

/**
 * toString是对象obj继承的属性，虽然delete命令返回true，但该属性并没有被删除，依然存在。
 * 这个例子还说明，即使delete返回true，该属性依然可能读取到值
 */
var obj2 = {};
console.log("删除继承的属性", delete obj2.toString); // true
console.log("查看继承的属性还在", obj2.toString) // function toString() { [native code] }

/**
 * 属性是否存在：in 运算符.   in 前面可以是纯数字，会转换成字符串，其它不带引号的会被当成变量
 * in运算符的一个问题是，它不能识别哪些属性是对象自身的，哪些属性是继承的
 * 可以使用对象的hasOwnProperty方法判断一下，是否为对象自身的属性
 */
console.log("查看属性是否存在", "100" in obj, 1 in obj, "1" in obj, toString in obj, "toString" in obj);
console.log('检查是否为对象自身的属性 obj.hasOwnProperty("toString"):', obj.hasOwnProperty("toString"));

/**
 * 属性的遍历：for...in 循环
 * 它遍历的是对象所有可遍历（enumerable）的属性，会跳过不可遍历的属性
 * 它不仅遍历对象自身的属性，还遍历继承的属性
 */
console.log("属性for in的遍历");
for (var v in obj) {
  if (obj.hasOwnProperty(v)) {//一般都会在判断里增加对自身属性的判断，不要去打印继承的属性
    console.log("obj[", v, "]=", obj[v]);
  }
}
console.log("\n");

/**
 * with 语句(了解即可，不用)
 * 它的作用是操作同一个对象的多个属性时，提供一些书写的方便。
 */
var obj3 = { a: 0 };
with (obj3) {
  a = 1;
  c = 2;//with语句里面必须是对象已经存在的属性，否则就会创造一个全局变量
}
console.log("obj3.a=", obj3.a, "obj3.c=", obj3.c, "c=", c)
/**
 * with (obj) {
 * console.log(x);
 * }
 * 
 * 单纯从上面的代码块，根本无法判断到底是全局变量，还是对象obj的一个属性
 * 因此，建议不要使用with语句，可以考虑用一个临时变量代替with
 */
console.log("\n");


/**
 * 函数
 * 函数是一段可以反复调用的代码块。函数还能接受输入的参数，不同的参数会返回不同的值。
 */
//函数定义1
function print(arg) {
  console.log(arg);
}

//函数定义2
//采用函数表达式声明函数时，function命令后面不带有函数名。
//如果加上函数名，该函数名只在函数体内部有效，在函数体外部无效。
var print2 = function x(arg) { console.log(typeof x, arg); };
//这里x只在函数内部有效;x可以省略，这样叫匿名函数;匿名函数又称函数表达式
print2("2");
/**
 * 上面这种写法的用处有两个，一是可以在函数体内部调用自身，
 * 二是方便除错（除错工具显示函数调用栈时，将显示函数名，而不再显示这里是一个匿名函数）
 */

//函数定义3
//Function接受任意数量的参数，只有最后一个被认为是函数体,前面都是参数
var print3 = new Function("arg", "console.log(arg);");
print3("new Function 3");
//Function构造函数可以不使用new命令，返回结果完全一样
//总的来说，这种声明函数的方式非常不直观，几乎无人使用,不建议该声明方式

//函数的重复声明,函数调用就是传入参数，return一个表达式，默认返回undefined,递归就是函数调用自身
function f1() { console.log("函数声明1"); }
f1();//这里由于函数名的提升，类似变量提升，只会打印:函数声明2
function f1() { console.log("函数声明2"); }
f1();

/**
 * 第一等公民
 * JavaScript 语言将函数看作一种值，与其它值（数值、字符串、布尔值等等）地位相同。
 * 凡是可以使用值的地方，就能使用函数
 * 
 * 函数名的提升
 * JavaScript 引擎将函数名视同变量名，所以采用function命令声明函数时，整个函数会像变量声明一样，被提升到代码头部
 * f();
 * 
 * function f() {}
 * 
 * 表面上，上面代码好像在声明之前就调用了函数f。但是实际上，由于“变量提升”，
 * 函数f被提升到了代码头部，也就是在调用之前已经声明了
 * 但是，如果采用赋值语句定义函数，JavaScript 就会报错
 * 
 * f();
 * var f = function (){};
 * 
 * 等同于
 * 
 * var f;
 * f();//这里f是undefined的，所以会报错
 *  f = function () {};
 */

//看这个例子
f2();//这里函数名提升，我们会打印：函数名提升1
function f2() { console.log("函数名提升1"); }
f2();//这里不变
var f2 = function () { console.log("函数名提升2"); };
f2();//f2被更新了值，所以这里打印：函数名提升2
print("\n");
/**
 * 函数的属性
 * 函数的name属性返回函数的名字
 * 如果是通过变量赋值定义的函数，并且是匿名函数那么name属性返回变量名。
 * 
 * 函数的length属性返回函数预期传入的参数个数，即函数定义之中的参数个数
 * 不管调用时传入多少参数，函数的length属性不变
 * 
 * 函数的toString方法返回一个字符串，内容是函数的源码
 */
console.log("f2.name", f2.name);
var f3 = function () { };
console.log("f3.name", f3.name);
var f4 = function myFunc() { };
console.log("f4.name", f4.name, obj.name);//变量没有name属性

/**
 * 函数作用域
 * 分全局作用域，函数作用域，(ES6新增块级作用域)
 * ES5中块作用域声明的变量会当成全局变量使用
 * 
 * 函数内部的变量提升
 * 
 * 函数本身的作用域
 * 函数本身也是一个值，也有自己的作用域。它的作用域与变量一样，就是其声明时所在的作用域，与其运行时所在的作用域无关。
 */
var a = 1;
var x = function () {
  console.log("测试函数作用域", a);//这里的a只能是全局作用域的a,f5函数作用域的a是不能在这里生效的
};
function f5() {
  var a = 2;
  x();
}
f5(); // 1
print("\n");

/**
 * 函数参数
 * 函数运行的时候，有时需要提供外部数据，不同的外部数据会得到不同的结果，这种外部数据就叫参数。
 * 函数参数不是必需的，Javascript 允许省略参数
 * 
 * 传递方式
 *  函数参数如果是原始类型的值（数值、字符串、布尔值），传递方式是传值传递（passes by value）。
 *  这意味着，在函数体内修改参数值，不会影响到函数外部
 * 
 *  如果函数参数是复合类型的值（数组、对象、其他函数），传递方式是传址传递（pass by reference）。
 *  也就是说，传入函数的原始值的地址，因此在函数内部修改参数，将会影响到原始值
 * 
 * 注意，如果函数内部修改的，不是参数对象的某个属性，而是替换掉整个参数，这时不会影响到原始值
 * 
 * 同名参数
 * 如果有同名的参数，则取最后出现的那个值,即使后面的参数没有值或被省略，也是以其为准。
 */
function f6(a, a) {
  console.log("同名参数取最后 a=", a);

  //要想获得第一个参数的值，则需要用到arguments对象
  console.log("同名参数取最后 arguments[0]=", arguments[0]);
}
f6(1);

/**
 * 函数的arguments对象
 * 由于 JavaScript 允许函数有不定数目的参数，所以需要一种机制，可以在函数体内部读取所有参数。这就是arguments对象的由来。
 * arguments对象包含了函数运行时的所有参数，arguments[0]就是第一个参数，arguments[1]就是第二个参数，
 * 以此类推。这个对象只有在函数体内部，才可以使用
 * 正常模式下，arguments对象可以在运行时修改。
 * 严格模式下，arguments对象是一个只读对象，修改它是无效的，但不会报错
 * 
 * 通过arguments对象的length属性，可以判断函数调用时到底带几个参数。
 * 
 * 需要注意的是，虽然arguments很像数组，但它是一个对象。
 * 数组专有的方法（比如slice和forEach），不能在arguments对象上直接使用。
 * 
 * 如果要让arguments对象使用数组方法，真正的解决方法是将arguments转为真正的数组
 * var args = Array.prototype.slice.call(arguments);
 * 
 * var args = [];
 * for (var i = 0; i < arguments.length; i++) {
 *   args.push(arguments[i]);
 * }
 * 
 * arguments对象带有一个callee属性，返回它所对应的原函数
 * 这个属性在严格模式里面是禁用的，因此不建议使用。
 */
function f7(a, b) {
  // 'use strict'; // 开启严格模式,,这个必须放在函数体首行位置，否则无效

  console.log("arguments.length=", arguments.length);

  console.log("arguments[0]=", arguments[0]);
  console.log("arguments[1]=", arguments[1]);
  console.log("arguments[2]=", arguments[2]);
  console.log("arguments[3]=", arguments[3]);

  //严格模式下，arguments对象是一个只读对象，修改它是无效的，但不会报错
  arguments[0] = 1;
  arguments[1] = 2;

  // callee 属性
  console.log("arguments.callee=", arguments.callee, arguments.callee === f7);

  return a + b;
}
console.log("修改arguments对象f7(10, 20, 30, 40)=", f7(10, 20, 30, 40, 50));
print("\n");
/**
 * 函数的其他知识点
 * 一般函数内部能访问外面局的变量，但是外面却不能访问到函数内部的局部变量
 * 
 * 闭包closure
 * 可以把闭包简单理解成“定义在一个函数内部的函数
 * 
 * 闭包的最大用处有两个
 *  一个是可以读取函数内部的变量，
 *  另一个就是让这些变量始终保持在内存中，即闭包可以使得它诞生环境一直存在
 * 
 * 注意，外层函数每次运行，都会生成一个新的闭包，而这个闭包又会保留外层函数的内部变量，所以内存消耗很大。
 * 因此不能滥用闭包，否则会造成网页的性能问题
 * 
 * 立即调用的函数表达式
 * 有时，我们需要在定义函数之后，立即调用该函数。这时，你不能在函数的定义之后加上圆括号，这会产生语法错误
 * 产生这个错误的原因是，function这个关键字即可以当作语句，也可以当作表达式
 * 为了避免解析上的歧义，JavaScript 引擎规定，如果function关键字出现在行首，一律解释成语句。
 * 因此，JavaScript 引擎看到行首是function关键字之后，认为这一段都是函数的定义，不应该以圆括号结尾，所以就报错了。
 * 解决方法就是不要让function出现在行首，让引擎将其理解成一个表达式。最简单的处理，就是将其放在一个圆括号里面。
 * 
 * (function(){  code  }());
 *    或者 
 * (function(){  code  })();
 */

/**
 * eval 命令
 * eval命令接受一个字符串作为参数，并将这个字符串当作语句执行。
 * 
 * eval命令可以修改了外部变量的值。由于这个原因，eval有安全风险
 */

var evalA = 2;
eval('evalA = 1;');
console.log("evalA=", evalA);

//为了防止这种风险，JavaScript规定，如果使用严格模式，eval内部声明的变量，不会影响到外部作用域
//不过，即使在严格模式下，eval依然可以读写当前作用域的变量
(function () {
  'use strict'
  eval('console.log("evalA=", evalA);var evalB = 1;');
  console.log("typeof evalB=", typeof evalB);

  var evalC = 1;
  eval('evalC = 3;');
  console.log("evalC=", evalC);//即使严格模式还是改写了外部变量
  //总之，eval的本质是在当前作用域之中，注入代码。由于安全风险和不利于 JavaScript 引擎优化执行速度，所以一般不推荐使用
})();
print("\n");
/**
 * eval 的别名调用
 * 
 * var m = eval;
 * m('var x = 1');
 * x // 1
 * 
 * 上面代码中，变量m是eval的别名。静态代码分析阶段，引擎分辨不出m('var x = 1')执行的是eval命令。
 * 
 * 为了保证eval的别名不影响代码优化，JavaScript 的标准规定，凡是使用别名执行eval，eval内部一律是全局作用域
 * eval的别名调用的形式五花八门，只要不是直接调用，都属于别名调用，因为引擎只能分辨eval()这一种形式是直接调用
 * 
 * eval.call(null, '...')
 * window.eval('...')
 * (1, eval)('...')
 * (eval, eval)('...')
 */
//尽量还是别用eval，存在安全风险

/**
 * 数组
 * 数组（array）是按次序排列的一组值。每个值的位置都有编号（从0开始），整个数组用方括号表示。
 * 
 * 本质上，数组属于一种特殊的对象。typeof运算符会返回数组的类型是object
 * 数组的特殊性体现在，它的键名是按次序排列的一组整数（0，1，2...）
 * 数组的键名其实也是字符串。之所以可以用数值读取，是因为非字符串的键名会被转为字符串。
 * 对象有两种读取成员的方法：点结构（object.key）和方括号结构（object[key]）。但是，对于数值的键名，不能使用点结构
 * 
 * 其实，如果对象的键名是数值的话也只能用方括号结构访问
 * 
 * 数组的length属性，返回数组的成员数量
 * JavaScript 使用一个32位整数，保存数组的元素个数 2^32-1个上限
 * 只要是数组，就一定有length属性。该属性是一个动态的值，等于键名中的最大整数加上1
 * length属性是可写的。如果人为设置一个小于当前成员个数的值，该数组的成员会自动减少到length设置的值
 * 清空数组的一个有效方法，就是将length属性设为0
 * 
 * 如果人为设置length大于当前元素个数，则数组的成员数量会增加到这个值，新增的位置都是空位
 * 
 * 值得注意的是，由于数组本质上是一种对象，所以可以为数组添加属性，但是这不影响length属性的值
 * 如果数组的键名是添加超出范围的数值，该键名会自动转为字符串。
 * 
 * in 运算符 判断数组某个键名是否存在 如果是undefined也会返回false
 * for in遍历数组
 * 但是，for...in不仅会遍历数组所有的数字键，还会遍历非数字键
 * 最好使用 for(var i = 0; i < arra.length; i++)
 * 
 * 数组的forEach方法，也可以用来遍历数组
 * 
 * 数组的空位
 */
var arr = ['a', 'b', 'c'];//声明加赋值
console.log("arr = ", arr);

var arr1 = [];//声明
arr1[0] = 'a';//后赋值
arr1[1] = 'b';
arr1[4] = 'c';
console.log("arr1 = ", arr1, typeof arr, arr.length);

arr.length = 2;
console.log("减小length", arr);

arr.length = 3;
console.log("增大length", arr, arr[2]);

var arr2 = [];
arr2[Math.pow(2, 32)] = "a";
console.log("arr2.length=", arr2.length, "arr2[Math.pow(2, 32)]=", arr2[Math.pow(2, 32)]);
console.log("键名 in", arr, 2 in arr, "0" in arr);
for (var v in arr) {
  console.log("遍历1 arr[", v, "]=", arr[v]);
}
for (var i = 0; i < arr.length; i++) {
  console.log("遍历2 arr[", i, "]=", arr[i]);
}
arr.forEach(function (val, i) {
  console.log("遍历3 arr[", i, "]=", val);
});

var arr3 = [0, 1, 2,];//最后一个逗号不会产生空位
console.log("数组空位 arr3[1]=", arr3[1], arr3.length);
delete arr3[1];//产生空位
console.log("数组空位 arr3[1]=", arr3[1], arr3.length, Object.keys(arr3));
//空位和undefined有点不一样，如果一个值被设定为undefined，
arr3[1] = undefined;//设定空位为undefined
console.log("查看数组keys =", Object.keys(arr3));

/**
 * 类似数组的对象
 * 如果一个对象的所有键名都是正整数或零，并且有length属性，那么这个对象就很像数组，语法上称为“类似数组的对象”（array-like object）
 * 
 * “类似数组的对象”的根本特征，就是具有length属性。只要有length属性，就可以认为这个对象类似于数组。
 * 但是有一个问题，这种length属性不是动态值，不会随着成员的变化而变化
 * 
 * 典型的“类似数组的对象”是函数的arguments对象，以及大多数 DOM 元素集，还有字符串
 * 
 * 类似数组要循环遍历的话，用：
 * Array.prototype.forEach.call('abc', function (chr) {
 *    console.log(chr);
 * });
 * 会比较慢，还是建议转数组再操作：
 * var arr = Array.prototype.slice.call(arrayLike);
 */

console.log("3 <= 4 - 1", 3 == 4 - 1)