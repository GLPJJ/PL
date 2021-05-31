/**
 * 面向对象编程
 * 
 * 实例对象与new命令
 * this关键字
 * 对象的继承
 * Object对象的相关方法
 * 严格模式
 */

// 典型的面向对象编程语言（比如 C++ 和 Java），都有“类”（class）这个概念。所谓“类”就是对象的模板，对象就是“类”的实例。但是
// JavaScript 语言的对象体系，不是基于“类”的，而是基于构造函数（constructor）和原型链（prototype）

// new命令的作用，就是执行构造函数，返回一个实例对象
var Vehicle = function (p) {
  'use strict';//构造函数使用严格模式，必须跟new一起使用
  this.price = p;
};

var v = new Vehicle(500);
console.log("new 对象", v.price);
//忘记调用new,this变成一个全局对象。。
try {
  var v1 = Vehicle(600);
  console.log("new 对象", v1.price);
} catch (error) {
  console.log(error);
}

/**

new 命令的原理
使用new命令时，它后面的函数依次执行下面的步骤。

创建一个空对象，作为将要返回的对象实例。
将这个空对象的原型，指向构造函数的prototype属性。
将这个空对象赋值给函数内部的this关键字。
开始执行构造函数内部的代码。

也就是说，构造函数内部，this指的是一个新生成的空对象，所有针对this的操作，都会发生在这个空对象上。
构造函数之所以叫“构造函数”，就是说这个函数的目的，就是操作一个空对象（即this对象），将其“构造”为需要的样子。
如果构造函数内部有return语句，而且return后面跟着一个对象，new命令会返回return语句指定的对象；
否则，就会不管return语句，返回this对象

但是，如果return语句返回的是一个跟this无关的新对象，new命令会返回这个新对象，而不是this对象。
这一点需要特别引起注意

另一方面，如果对普通函数（内部没有this关键字的函数）使用new命令，则会返回一个空对象

 */
// new命令简化的内部流程，可以用下面的代码表示。
function _new(/* 构造函数 */ constructor, /* 构造函数参数 */ params) {
  // 将 arguments 对象转为数组
  var args = [].slice.call(arguments);
  // 取出构造函数
  var constructor = args.shift();
  // 创建一个空对象，继承构造函数的 prototype 属性
  var context = Object.create(constructor.prototype);
  // 执行构造函数
  var result = constructor.apply(context, args);
  // 如果返回结果是对象，就直接返回，否则返回 context 对象
  return (typeof result === 'object' && result != null) ? result : context;
}

// new.target
// 函数内部可以使用new.target属性。如果当前函数是new命令调用，new.target指向当前函数，否则为undefined。

function funcNetTarget() {
  // 使用这个属性，可以判断函数调用的时候，是否使用new命令。
  console.log("funcNetTarget", new.target === funcNetTarget);
}

funcNetTarget(); // false
new funcNetTarget(); // true

// Object.create() 创建实例对象
// 构造函数作为模板，可以生成实例对象。但是，有时拿不到构造函数，只能拿到一个现有的对象。
// 我们希望以这个现有的对象作为模板，生成新的实例对象，这时就可以使用Object.create()方法

// this
// 简单说，this就是属性或方法“当前”所在的对象。

/*
var obj = { foo:  5 };
上面的代码将一个对象赋值给变量obj。JavaScript 引擎会先在内存里面，生成一个对象{ foo: 5 }，然后把这个对象的内存地址赋值给变量obj。也就是说，变量obj是一个地址（reference）。后面如果要读取obj.foo，引擎先从obj拿到内存地址，然后再从该地址读出原始的对象，返回它的foo属性。
 
原始的对象以字典结构保存，每一个属性名都对应一个属性描述对象。举例来说，上面例子的foo属性，实际上是以下面的形式保存的。
 
{
  foo: {
    [[value]]: 5
    [[writable]]: true
    [[enumerable]]: true
    [[configurable]]: true
  }
}
注意，foo属性的值保存在属性描述对象的value属性里面
这样的结构是很清晰的，问题在于属性的值可能是一个函数。
var obj = { foo: function () {} };
这时，引擎会将函数单独保存在内存中，然后再将函数的地址赋值给foo属性的value属性。
{
  foo: {
    [[value]]: 函数的地址
    ...
  }
}
由于函数是一个单独的值，所以它可以在不同的环境（上下文）执行
 
this主要有以下几个使用场合
全局环境使用this，它指的就是顶层对象window (nodejs 没有这个)
*/
// console.log("this == window", this == window);

/*
var obj = {
    foo: function () {
        console.log(this);
    }
};
obj.foo() // obj
但是，下面这几种用法，都会改变this的指向。
情况一
(obj.foo = obj.foo)(); // window
// 情况二
(false || obj.foo)(); // window
// 情况三
(1, obj.foo)(); // window

如果this所在的方法不在对象的第一层，这时this只是指向当前一层的对象，而不会继承更上面的层。
var a = {
  p: 'Hello',
  b: {
    m: function() {
      console.log(this.p);
    }
  }
};
a.b.m() // undefined
上面代码中，a.b.m方法在a对象的第二层，该方法内部的this不是指向a，而是指向a.b，因为实际执行的是下面的代码
var b = {
  m: function() {
   console.log(this.p);
  }
};
var a = {
  p: 'Hello',
  b: b
};
(a.b).m() // 等同于 b.m()

避免多层 this
由于this的指向是不确定的，所以切勿在函数中包含多层的this
    使用一个变量固定this的值，然后内层函数调用这个变量，是非常常见的做法，请务必掌握。
避免数组处理方法中的 this
避免回调函数中的 this
*/

// 绑定 this 的方法
// JavaScript 提供了call、apply、bind这三个方法，来切换/固定this的指向。

//call 示例
var obj = {};
var fCall = function () {
  console.log("fCall this=", this);
  return this;
};

// f() === window // true //nodejs 环境没有window,由global代替
console.log("fCall() === global", fCall() === global);
console.log("fCall.call(obj) === obj", fCall.call(obj) === obj); // true
// call方法的参数，应该是一个对象。如果参数为空、null和undefined，则默认传入全局对象
// 传入的原始值也会转成对象
// call方法还可以接受多个参数
// call的第一个参数就是this所要指向的那个对象，后面的参数则是函数调用时所需的参数
function fAdd(a) { return a + this.b; }
var obj1 = { b: 2 };
console.log("obj1.b =", obj1.b);
console.log("call 示例 fAdd.call()", fAdd.call(obj1, 1));

// call方法的一个应用是调用对象的原生方法
var obj2 = {};
console.log("obj2.hasOwnProperty('toString')", obj2.hasOwnProperty('toString')); // false
// 覆盖掉继承的 hasOwnProperty 方法
obj2.hasOwnProperty = function () {
  return true;
};
console.log("obj2.hasOwnProperty('toString')", obj2.hasOwnProperty('toString')); // false
console.log("Object.prototype.hasOwnProperty.call(obj2, 'toString')"
  , Object.prototype.hasOwnProperty.call(obj2, 'toString')); // false


//applay 示例
// apply方法的作用与call方法类似，也是改变this指向，然后再调用该函数。唯一的区别就是，
// 它接收一个数组作为函数执行时的参数，使用格式如下。
// func.apply(thisValue, [arg1, arg2, ...])
console.log("apply 示例 找出最大值 ", Math.max.apply(null, [22, 4, 5, 200, 33]));

// bind 示例
// bind方法用于将函数体内的this绑定到某个对象，然后返回一个新函数
// bind不仅可以绑定this，还可以绑定参数
function fAdd1(a, b) { return a + b; }
var fAdd2 = fAdd1.bind(null, 2);//这里绑定了参数a为2
console.log("绑定对象和参数", fAdd2(10));

/*
每一次返回一个新函数
bind方法每运行一次，就返回一个新函数，这会产生一些问题。比如，监听事件的时候，不能写成下面这样。
element.addEventListener('click', o.m.bind(o));
上面代码中，click事件绑定bind方法生成的一个匿名函数。这样会导致无法取消绑定，所以，下面的代码是无效的。

element.removeEventListener('click', o.m.bind(o));
正确的方法是写成下面这样：

var listener = o.m.bind(o);
element.addEventListener('click', listener);
//  ...
element.removeEventListener('click', listener);
*/
var obj2 = { a: 4, b: 5 };
function fAdd3() {
  return this.a + this.b;
}
console.log("bind 示例", (fAdd3.bind(obj2))());

//对象的继承
// 构造函数的缺点 ，同一个构造函数new出来的对象，无法共享对象的属性和方法
// prototype 属性的作用
// JavaScript 继承机制的设计思想就是，原型对象的所有属性和方法，都能被实例对象共享
// JavaScript 规定，每个【函数】都有一个prototype属性，指向一个对象。
function func1() { };
console.log("函数的prototype的类型", typeof func1.prototype);
// 对于普通函数来说，该属性基本无用。但是，对于构造函数来说，生成实例的时候，该属性会自动成为实例对象的原型
function Cat(name) {
  this.name = name;
}
Cat.prototype.color = "White";
var catA = new Cat("A");
var catB = new Cat("B");
console.log("构造函数原型方法 name:", catA.name, catB.name);
console.log("构造函数原型方法1 color:", catA.color, catB.color);
catA.color = "Black";
console.log("构造函数原型方法2 color:", catA.color, catB.color);
Cat.prototype.color = "Gray";
console.log("构造函数原型方法3 color:", catA.color, catB.color);

// 总结一下，原型对象的作用，就是定义所有实例对象共享的属性和方法。
// 这也是它被称为原型对象的原因，而实例对象可以视作从原型对象衍生出来的子对象
// JavaScript 规定，所有对象都有自己的原型对象（prototype）。一方面，任何一个对象，
// 都可以充当其他对象的原型；另一方面，由于原型对象也是对象，所以它也有自己的原型。因此，就会形成一个“原型链”（prototype chain）
// 所有对象的原型都指向Object.prototype。而Object.prototype的原型对象是null
console.log("Object.getPrototypeOf(Object.prototype)", Object.getPrototypeOf(Object.prototype));

// constructor 属性
// prototype对象有一个constructor属性，默认指向prototype对象所在的构造函数
// constructor属性的作用是，可以得知某个实例对象，到底是哪一个构造函数产生的
function A() { }
console.log("构造函数constructor属性,A.prototype.constructor === A", A.prototype.constructor === A);
var a = new A();//这里调用了A.prototype.constructor
console.log("构造函数constructor属性,a.constructor === A", a.constructor === A);
// 修改原型对象时，一般要同时修改constructor属性的指向
function B() { }
B.prototype = {

};
//这里由于只是修改了B的原型对象，并没有修改原型对象的constructor，导致B的构造指向了Object
console.log("修改原型对象后必须也要修改constructor属性,B.prototype.constructor === Object"
  , B.prototype.constructor === Object);
/*
修改原型对象

  // 坏的写法
C.prototype = {
  method1: function (...) { ... },
  // ...
};

// 好的写法
C.prototype = {
  constructor: C,
  method1: function (...) { ... },
  // ...
};

// 更好的写法
C.prototype.method1 = function (...) { ... };
*/
