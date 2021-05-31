/**
 * 
 * 开始新的JavaScript学习
 * 
 * 本篇内容：
 * Object对象
 * 属性描述对象
 * Array对象
 * 包装对象
 * Boolean对象
 * Number对象
 * String对象
 * Math对象
 * Date对象
 * RegExp对象
 * JSON对象
 * 
 */

/**
 * Object对象
 * Object对象本身的方法-静态方法
 *     所谓”本身的方法“就是直接定义在Object对象的方法
 * 
 * Object的实例方法
 *     所谓实例方法就是定义在Object原型对象Object.prototype上的方法。它可以被Object实例直接使用。
 */

var obj1 = Object();
// 等同于
var obj2 = Object(undefined);//不建议这样写，累赘
var obj3 = Object(null);//不建议这样写，累赘
console.log("obj2 instanceof Object:", obj2 instanceof Object);

/**
 * Object函数的参数是各种原始类型的值，转换成对象就是原始类型值对应的包装对象。
 * 
    var obj = Object(1);
    obj instanceof Object // true
    obj instanceof Number // true

    var obj = Object('foo');
    obj instanceof Object // true
    obj instanceof String // true

    var obj = Object(true);
    obj instanceof Object // true
    obj instanceof Boolean // true

    如果Object方法的参数是一个对象，它总是返回该对象，即不用转换
 */
//自定义判断是否对象的方法
function isObject(value) {
    return value === Object(value);
}

/**
 * 注意，通过var obj = new Object()的写法生成新对象，与字面量的写法var obj = {}是等价的。
 * 或者说，后者只是前者的一种简便写法
 * 
 * 虽然用法相似,Object(value)与new Object(value)两者的语义是不同的，
 * Object(value)表示将value转成一个对象，new Object(value)则表示新生成一个对象，它的值是value。
 */

/**
 * Object.keys方法和Object.getOwnPropertyNames方法都用来遍历对象的属性
 * 
 * 对于一般的对象来说，Object.keys()和Object.getOwnPropertyNames()返回的结果是一样的
 * Object.keys方法只返回可枚举的属性，
 * Object.getOwnPropertyNames方法还返回不可枚举的属性名。
 * 
 * 一般情况下，几乎总是使用Object.keys方法，遍历数组的属性
 */
var arra = [1, 2, 3];
console.log("获取对象属性", Object.keys(arra), Object.getOwnPropertyNames(arra));
console.log("\n");
/**
 * 其他对象静态方法
 * 
    （1）对象属性模型的相关方法
        Object.getOwnPropertyDescriptor()：获取某个属性的描述对象。
        Object.defineProperty()：通过描述对象，定义某个属性。
        Object.defineProperties()：通过描述对象，定义多个属性。
    （2）控制对象状态的方法
        Object.preventExtensions()：防止对象扩展。
        Object.isExtensible()：判断对象是否可扩展。
        Object.seal()：禁止对象配置。
        Object.isSealed()：判断一个对象是否可配置。
        Object.freeze()：冻结一个对象。
        Object.isFrozen()：判断一个对象是否被冻结。
    （3）原型链相关方法
        Object.create()：该方法可以指定原型对象和属性，返回一个新的对象。
        Object.getPrototypeOf()：获取对象的Prototype对象。
 */

/**
 * 对象的实例方法
   
   Object实例对象的方法，主要有以下六个。
       Object.prototype.valueOf()：返回当前对象对应的值。
       Object.prototype.toString()：返回当前对象对应的字符串形式。
       Object.prototype.toLocaleString()：返回当前对象对应的本地字符串形式。
       Object.prototype.hasOwnProperty()：判断某个属性是否为当前对象自身的属性，还是继承自原型对象的属性。
       Object.prototype.isPrototypeOf()：判断当前对象是否为另一个对象的原型。
       Object.prototype.propertyIsEnumerable()：判断某个属性是否可枚举。
            实例对象的propertyIsEnumerable()方法返回一个布尔值，用来判断某个属性是否可遍历。
            注意，这个方法只能用于判断对象自身的属性，对于继承的属性一律返回false。
*/

//valueOf方法的作用是返回一个对象的“值”，默认情况下返回对象本身。数据类型转换的时候会用到它

// toString方法是返回一个对象的字符串形式
// 数组、字符串、函数、Date 对象都分别部署了自定义的toString方法，覆盖了Object.prototype.toString方法
// 我们也可以自定定义toString方法覆盖Object.prototype.toString方法
var my = {
    toString: function () {
        return "Glp";
    }
};
// var my = new Object();
// my.toString = function () {
//     return "Glp";
// };
console.log("" + my, Object.prototype.toString.call(my));

//Object.prototype.toString可以实现比type更精确的类型判断
function myType(val) {
    var str = Object.prototype.toString.call(val);
    var strs = str.match(/\[object (.*)\]/);
    console.log(str, strs);

    var ret = strs[1].toLowerCase();
    console.log(ret);

    return ret;
}

myType({}); // "object"
myType([]); // "array"
myType(5); // "number"
myType(null); // "null"
myType(); // "undefined"
myType(/abcd/); // "regex"
myType(new Date()); // "date"

['Null',
    'Undefined',
    'Object',
    'Array',
    'String',
    'Number',
    'Boolean',
    'Function',
    'RegExp'
].forEach(function (t, i) {
    myType['is' + t] = function (o) {
        return myType(o) === t.toLowerCase();
    };
});

console.log("myType.isNull(null)=", myType.isNull(null));

/**
 * 属性描述对象
 * 
 */
//下面是属性描述对象的一个例子
var proto = {
    value: 123,//value是该属性的属性值，默认为undefined
    writable: false,//writable是一个布尔值，表示属性值（value）是否可改变（即是否可写），默认为true。

    //enumerable是一个布尔值，表示该属性是否可遍历，默认为true
    //如果设为false，会使得某些操作（比如for...in循环、Object.keys()）跳过该属性
    enumerable: true,

    //configurable是一个布尔值，表示可配置性，默认为true。
    //如果设为false，将阻止某些操作改写该属性，比如无法删除该属性，
    //也不得改变该属性的属性描述对象（value属性除外）。
    //也就是说，configurable属性控制了属性描述对象的可写性
    configurable: false,
    get: undefined,//get是一个函数，表示该属性的取值函数（getter），默认为undefined
    set: undefined//set是一个函数，表示该属性的存值函数（setter），默认为undefined
}

var obj = { p: 'a' };
console.log("获取属性描述", Object.getOwnPropertyDescriptor(obj, 'p'));
//注意，Object.getOwnPropertyDescriptor()方法只能用于对象自身的属性，不能用于继承的属性

// Object.getOwnPropertyNames方法返回一个数组，成员是参数对象自身的全部属性的属性名，不管该属性是否可遍历
var obj1 = Object.defineProperties({}, {
    p1: { value: 1, enumerable: true },
    p2: { value: 2, enumerable: false }
});
console.log("Object.getOwnPropertyNames", Object.getOwnPropertyNames(obj1), Object.keys(obj1));

var obj2 = Object.defineProperty({}, "p", {
    value: 123,
    writable: false,
    enumerable: true,
    configurable: false,

    //注意，一旦定义了取值函数get（或存值函数set），
    //就不能将writable属性设为true，或者同时定义value属性，否则会报错
    // get: undefined,
    // set: undefined

    /*
    var obj = {};
    Object.defineProperty(obj, 'p', {
    value: 123,
    get: function() { return 456; }
    });
    // TypeError: Invalid property.
    // A property cannot both have accessors and be writable or have a value

    Object.defineProperty(obj, 'p', {
    writable: true,
    get: function() { return 456; }
    });
    // TypeError: Invalid property descriptor.
    // Cannot both specify accessors and a value or writable attribute
    */
});
console.log("Object.defineProperty 不可写1", obj2.p);
obj2.p = 200;//这里因为定义属性的时候writable属性是false，所以不能写入成功
console.log("Object.defineProperty 不可写2", obj2.p);

/*
元属性
    value属性是目标属性的值

    writable属性是一个布尔值，决定了目标属性的值（value）是否可以被改变
    如果是false，在'use strict'严格模式会报错，普通只是默默的写入失败

    enumerable（可遍历性）返回一个布尔值，表示目标属性是否可遍历
    具体来说，如果一个属性的enumerable为false，下面三个操作不会取到该属性。
        for..in循环
        Object.keys方法
        JSON.stringify方法

        注意，for...in循环包括继承的属性，Object.keys方法不包括继承的属性

        如果需要获取对象自身的所有属性，不管是否可遍历，可以使用Object.getOwnPropertyNames方法。
        JSON.stringify方法会排除enumerable为false的属性，有时可以利用这一点。
            如果对象的 JSON 格式输出要排除某些属性，就可以把这些属性的enumerable设为false。

    configurable(可配置性）返回一个布尔值，决定了是否可以修改属性描述对象
        obj.p的configurable为false。然后，改动value、writable、enumerable、configurable，结果都报错。
        注意，writable只有在false改为true会报错，true改为false是允许的

        至于value，只要writable和configurable有一个为true，就允许改动
        另外，configurable为false时，直接目标属性赋值，不报错，但不会成功;如果是严格模式，还会报错。
        
        可配置性决定了目标属性是否可以被删除（delete）

    存取器
        除了直接定义以外，属性还可以用存取器（accessor）定义。其中，存值函数称为setter，
        使用属性描述对象的set属性；取值函数称为getter，使用属性描述对象的get属性。
*/
var obj3 = Object.defineProperty({}, 'p', {
    get: function () {
        return 'getter';
    },
    set: function (value) {
        console.log('setter: ' + value);
    }
});

console.log(obj3.p); // "getter"
obj3.p = 123; // "setter: 123"

// JavaScript 还提供了存取器的另一种写法。
var obj4 = {//这个写法跟obj3是等价的
    get p() {
        return 'getter';
    },
    set p(value) {
        console.log('setter: ' + value);
    }
};
//注意，取值函数get不能接受参数，存值函数set只能接受一个参数（即属性的值）
console.log("\n");

/**
 * 对象的拷贝
 */
var extend = function (to, from) {
    for (var property in from) {
        to[property] = from[property];
    }
    return to;
};
var copy1 = extend({}, {
    a: 1
});
var src2 = {
    get a() { return 1 }
};
console.log("对象的拷贝1:", src2.a, copy1);
var copy2 = extend({}, src2);
src2.a = 10;
copy2.a = 10;
console.log("对象的拷贝2:", src2.a, copy2.a, copy2);//拷贝后的对象可以对a值进行修改，

//为了解决这个问题，我们可以通过Object.defineProperty方法来拷贝属性
var extend2 = function (to, from) {
    for (var property in from) {
        if (!from.hasOwnProperty(property)) continue;

        //这里把from的属性拷贝到to
        Object.defineProperty(
            to,
            property,
            Object.getOwnPropertyDescriptor(from, property)
        );
    }

    return to;
};
var copy3 = extend2({}, src2);
copy3.a = 20;
console.log("对象的拷贝3:", src2.a, copy3.a, copy3);

/**
 * 控制对象状态
 * 有时需要冻结对象的读写状态，防止对象被改变。JavaScript 提供了三种冻结方法，
 * 最弱的一种是Object.preventExtensions，其次是Object.seal，最强的是Object.freeze
 *      Object.preventExtensions方法可以使得一个对象无法再添加新的属性
 *      Object.isExtensible方法用于检查一个对象是否使用了Object.preventExtensions方法。
 *          也就是说，检查是否可以为一个对象添加属性
 * 
 *      Object.seal方法使得一个对象既无法添加新属性，也无法删除旧属性
 *      Object.isSealed方法用于检查一个对象是否使用了Object.seal方法
 * 
 *      Object.freeze方法可以使得一个对象无法添加新属性、无法删除旧属性、也无法改变属性的值，使得这个对象实际上变成了常量
 *      Object.isFrozen方法用于检查一个对象是否使用了Object.freeze方法
 */

/**
 * 局限性
 * 上面的三个方法锁定对象的可写性有一个漏洞：可以通过改变原型对象，来为对象增加属性
 */
var obj = new Object();
Object.preventExtensions(obj);

var proto = Object.getPrototypeOf(obj);
proto.t = 'hello';
console.log("改变原型对象，来为对象增加属性", obj.t);
//一种解决方案是，把obj的原型也冻结住

/**
 * 另外一个局限是，如果属性值是对象，上面这些方法只能冻结属性指向的对象，而不能冻结对象本身的内容。
 */
var obj1 = {
    foo: 1,
    bar: ['a', 'b']
};
Object.freeze(obj1);

obj1.bar.push('c');
// obj1.bar // ["a", "b", "c"]
console.log("属性值是对象,无法确保内容不变", obj.t);
//综上，阻止扩张，密封，冰冻，并不能很好的使用。

/**
 * Array对象
 * Array是 JavaScript 的原生对象，同时也是一个构造函数，可以用它生成新的数组
 * 
 * var arr = new Array(2);
 * // 等同于
 * var arr = Array(2);
 */
var arra = new Array(2);
console.log("arra = ", arra, arra.length);

/*
    Array构造函数行为多变
        // 无参数时，返回一个空数组
        new Array() // []

        // 单个正整数参数，表示返回的新数组的长度
        new Array(1) // [ empty ]
        new Array(2) // [ empty x 2 ]

        // 非正整数的数值作为参数，会报错
        new Array(3.2) // RangeError: Invalid array length
        new Array(-3) // RangeError: Invalid array length

        // 单个非数值（比如字符串、布尔值、对象等）作为参数，
        // 则该参数是返回的新数组的成员
        new Array('abc') // ['abc']
        new Array([1]) // [Array[1]]

        // 多参数时，所有参数都是返回的新数组的成员
        new Array(1, 2) // [1, 2]
        new Array('a', 'b', 'c') // ['a', 'b', 'c']

    可以看到，Array作为构造函数，行为很不一致。因此，不建议使用它生成新数组，直接使用数组字面量是更好的做法
        // bad
        var arr = new Array(1, 2);
        // good
        var arr = [1, 2];

    注意，如果参数是一个正整数，返回数组的成员都是空位。虽然读取的时候返回undefined，
    但实际上该位置没有任何值。虽然可以取到length属性，但是取不到键名
*/
var a = new Array(3);
var b = [undefined, undefined, undefined];
console.log("Array 和 数组字面量创建数组的比较", a.length, b.length, a[0], b[0], 0 in a, 0 in b);

/**
 * 数组静态方法
 * 
 * Array.isArray方法返回一个布尔值，表示参数是否为数组。它可以弥补typeof运算符的不足
 */
console.log(typeof a, Array.isArray(a));

/**
 * 数组实例方法
 * valueOf()，toString()
 * valueOf方法是一个所有对象都拥有的方法，表示对该对象求值。不同对象的valueOf方法不尽一致，数组的valueOf方法返回数组本身
 * toString方法也是对象的通用方法，数组的toString方法返回数组的字符串形式
 */
console.log("valueOf,toString", a.valueOf(), a.toString());

// push方法用于在数组的末端添加一个或多个元素，并返回添加新元素后的数组长度。注意，该方法会改变原数组
// pop方法用于删除数组的最后一个元素，并返回该元素。注意，该方法会改变原数组。
var c = [1, 2, 3];
console.log("push c=", c.push(4, 5), c);
console.log("pop c=", c.pop(), c);
// 对空数组使用pop方法，不会报错，而是返回undefined
console.log("pop 空数组", [].pop());
//push和pop结合使用，就构成了“后进先出”的栈结构（stack）

// shift方法用于删除数组的第一个元素，并返回该元素。注意，该方法会改变原数组
console.log("shift c=", c.shift(), c);
//push和shift结合使用，就构成了“先进先出”的队列结构（queue）

// unshift 方法用于在数组的第一个位置添加元素，并返回添加新元素后的数组长度。注意，该方法会改变原数组
console.log("unshift c=", c.unshift(6), c);

// join方法以指定参数作为分隔符，将所有数组成员连接为一个字符串返回。如果不提供参数，默认用逗号分隔
// 如果数组成员是undefined或null或空位，会被转成空字符串
console.log("join c=", c.join(), c.join("!"));

// 通过call方法，这个方法也可以用于字符串或类似数组的对象
console.log("call方法", Array.prototype.join.call("Hello", "#"));
var obj = { 0: 'a', 1: 'b', length: 2 };
console.log("call方法", Array.prototype.join.call(obj, '-'));

// concat方法用于多个数组的合并。它将新数组的成员，添加到原数组成员的后部，然后返回一个新数组，原数组不变
var d = [7, 8]
console.log("concat", c.concat(d), c, d, d.concat(9, 10, 11));

// 如果数组成员包括对象，concat方法返回当前数组的一个浅拷贝。所谓“浅拷贝”，指的是新数组拷贝的是对象的引用
var obj = { a: 1 };
var oldArray = [obj];
var newArray = oldArray.concat();
obj.a = 2;
console.log("concat 浅拷贝", obj.a, newArray[0].a);

// reverse方法用于颠倒排列数组元素，返回改变后的数组。注意，该方法将改变原数组
console.log("reverse " + d, d.reverse(), d);

// slice方法用于提取目标数组的一部分，返回一个新数组，原数组不变
// slice方法的一个重要应用，是将类似数组的对象转为真正的数组
var e = ['a', 'b', { a: 1 }];
var e2 = e.slice();
e[2].a = 2;
console.log("\nslice", e.slice(0), e.slice(1), e.slice(1, 2), e.slice(2, 6), e[2].a, e2[2].a);
// 最后一个例子slice没有参数，实际上等于返回一个原数组的拷贝(浅拷贝)

// splice方法用于删除原数组的一部分成员，并可以在删除的位置添加新的数组成员，
// 返回值是被删除的元素。注意，该方法会改变原数组
// arr.splice(start, count, addElement1, addElement2, ...);
// splice的第一个参数是删除的起始位置（从0开始），第二个参数是被删除的元素个数。
// 如果后面还有更多的参数，则表示这些就是要被插入数组的新元素
console.log("splice " + c, c.splice(1, 2), c);
var f = [10, 20, 30, 40, 50, 60];
// 如果只是单纯地插入元素，splice方法的第二个参数可以设为0
console.log("splice 单纯插入", f.splice(3, 0, 70));
// 如果只提供第一个参数，等同于将原数组在指定位置拆分成两个数组
console.log("splice 拆分两个", f.splice(3), f);

// sort方法对数组成员进行排序，默认是按照字典顺序排序。排序后，原数组将被改变
// sort方法不是按照大小排序，而是按照字典顺序。
// 也就是说，数值会被先转成字符串，再按照字典顺序进行比较，所以101排在11的前面
console.log("sort", f.sort(function (a, b) { return b - a; }));

// map方法将数组的所有成员依次传入参数函数，然后把每一次的执行结果组成一个新数组返回
console.log("map " + f, f.map(function (v, i, arra) { return v ** 2; }), f);//原数组没有变化
// map方法还可以接受第二个参数，用来绑定回调函数内部的this变量
// 如果数组有空位，map方法的回调函数在这个位置不会执行，会跳过数组的空位

// forEach方法与map方法很相似，也是对数组的所有成员依次执行参数函数。
// 但是，forEach方法不返回值，只用来操作数据。
// 这就是说，如果数组遍历的目的是为了得到返回值，那么使用map方法，否则使用forEach方法
console.log("forEach", f.forEach(function (v, i, arra) { v = arra[i] + i; console.log("forEach1", v) }), f);
// forEach方法也可以接受第二个参数，绑定参数函数的this变量
// 注意，forEach方法无法中断执行，总是会将所有成员遍历完。如果希望符合某种条件时，就中断遍历，要使用for循环
// forEach方法也会跳过数组的空位(跟map函数一样)

// filter方法用于过滤数组成员，满足条件的成员组成一个新数组返回
console.log("filter " + f, f.filter(function (v, i, arra) { return i <= 1; }));
// filter方法还可以接受第二个参数，用来绑定参数函数内部的this变量

// some方法是只要一个成员的返回值是true，则整个some方法的返回值就是true，否则返回false
// every方法是所有成员的返回值都是true，整个every方法才返回true，否则返回false
// 注意，对于空数组，some方法返回false，every方法返回true，回调函数都不会执行
// some和every方法还可以接受第二个参数，用来绑定参数函数内部的this变量
console.log("some and every", f.some(function (v, i, arra) { return v > 20 })
    , f.every(function (v, i, arra) { return v > 20 }));

/**
 * reduce方法和reduceRight方法依次处理数组的每个成员，最终累计为一个值。它们的差别是，
 * reduce是从左到右处理（从第一个成员到最后一个成员），reduceRight则是从右到左（从最后一个成员到第一个成员），
 * 其他完全一样
 */
console.log("reduce =", [1, 2, 3, 4].reduce(function (累积变量, 当前变量, 当前位置, 原数组) {
    return 累积变量 ** 当前变量;
}));
console.log("reduceRight =", [1, 2, 3, 4].reduceRight(function (累积变量, 当前变量, 当前位置, 原数组) {
    return 累积变量 ** 当前变量;
}));
// 如果要对累积变量指定初值，可以把它放在reduce方法和reduceRight方法的第二个参数
// 由于空数组取不到初始值，reduce方法会报错。这时，加上第二个参数，就能保证总是会返回一个值
console.log("reduce2 =", [].reduce(function (累积变量, 当前变量, 当前位置, 原数组) {
    console.log("reduce2 function", 累积变量, 当前变量, typeof 当前变量);//空数组这里不会执行
    return 累积变量 ** 当前变量;
}, 1));//不加入第二个值会报错

// indexOf方法返回给定元素在数组中第一次出现的位置，如果没有出现则返回-1
// indexOf方法还可以接受第二个参数，表示搜索的开始位置
// lastIndexOf方法返回给定元素在数组中最后一次出现的位置，如果没有出现则返回-1
// 注意，这两个方法不能用来搜索NaN的位置，即它们无法确定数组成员是否包含NaN 判断是由严格相等
var g = [1, 2, 3, '4', 5, NaN];
console.log("indexOf", g.indexOf(4), g.indexOf(2), g.indexOf(1, 3), g.indexOf(NaN));
console.log("lastIndexOf", g.lastIndexOf(4), g.lastIndexOf(1), g.lastIndexOf(1, 3));

/**
 * 包装对象
 */
// 所谓“包装对象”，就是分别与数值、字符串、布尔值相对应的Number、String、Boolean三个原生对象。
// 这三个原生对象可以把原始类型的值变成（包装成）对象
// Number、String和Boolean如果不作为构造函数调用（即调用时不加new），
// 常常用于将任意类型的值转为数值、字符串和布尔值
var objNum = new Number(1);//使用new创建一个对象
var objNum1 = Number("1");//如果不是用new，常常用于数值转换
var objStr = new String("2");
var objBoolean = new Boolean(true);
console.log("包装对象", typeof objNum, typeof objNum1, typeof objStr, typeof objBoolean);
// 包装对象的最大目的，首先是使得 JavaScript 的对象涵盖所有的值，其次使得原始类型的值可以方便地调用某些方法
// 包装对象都有valueOf 和 toString

// 原始类型与实例对象的自动转换
// 原始类型的值，可以自动当作包装对象调用，即调用包装对象的属性和方法。
// 这时，JavaScript 引擎会自动将原始类型的值转为包装对象实例，在使用后立刻销毁实例
console.log('"abc".length =', "abc".length);//自动转对象调用length方法,用完销毁
// 自动转换生成的包装对象是只读的，无法修改。所以，字符串无法添加新属性
var str = "123";
str.x = 1;
console.log("字符串自动包装对象只读", str.x);

// 除了原生的实例方法，包装对象还可以自定义方法和属性，供原始类型的值直接调用
String.prototype.double = function () {
    return this.valueOf() + this.valueOf();
}
Number.prototype.double = function () {
    return this.valueOf() + this.valueOf();
}
console.log("自定义方法", "123".double(), (123).double());//数字必须加括号才能调用

//Boolean对象
console.log("Booean 对象", !!new Boolean(false), !!new Boolean(false).valueOf(), Boolean(false));//false转换成对象判断为true

//Number对象
console.log("Number 对象", Number(true));
console.log("Number 静态属性", Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY
    , Number.MAX_VALUE, Number.MIN_VALUE, Number.MAX_SAFE_INTEGER, Number.MIN_SAFE_INTEGER);
// toString方法可以接受一个参数，表示输出的进制
console.log("Number toString", Number.prototype.toString.call(10, 2));//默认十进制
// toString方法只能将十进制的数，转为其他进制的字符串。如果要将其他进制的数，转回十进制，需要使用parseInt方法
// toFixed方法的参数为小数位数，有效范围为0到20，超出这个范围将抛出 RangeError 错误
console.log("Number toFixed 1", Number.prototype.toFixed.call(4.554, 2));//保留两位有效数字
console.log("Number toFixed 2", Number.prototype.toFixed.call(4.555, 2));//保留两位有效数字
console.log("Number toFixed 3", Number.prototype.toFixed.call(4.556, 2));//保留两位有效数字
console.log("Number toExponential", Number.prototype.toExponential.call(4.556, 1));//转为科学计数，保留有效数字1位
// toPrecision方法的参数为有效数字的位数，范围是1到21，超出这个范围会抛出 RangeError 错误。
// toPrecision方法用于四舍五入时不太可靠，跟浮点数不是精确储存有关
console.log("Number toPrecision", Number.prototype.toPrecision.call(174.556, 1));//转为指定位数的有效数字，保留有效数字1位
// 与其他对象一样，Number.prototype对象上面可以自定义方法，被Number的实例继承

//String对象
//静态方法String.fromCharCode
console.log("String对象", typeof "abcd", typeof new String("abcd"));
console.log("String对象 String.fromCharCode()", String.fromCharCode(48), String.fromCharCode(97));
// 注意，该方法不支持 Unicode 码点大于0xFFFF的字符，即传入的参数不能大于0xFFFF（即十进制的 65535）
// 这种现象的根本原因在于，码点大于0xFFFF的字符占用四个字节，而 JavaScript 默认支持两个字节的字符。
// 这种情况下，必须把0x20BB7拆成两个字符表示。
// 0x20BB7
var theChar = String.fromCharCode(0xD842, 0xDFB7) //0x20BB7
console.log("0x20BB7=", String.fromCharCode(0x20BB7), String.fromCharCode(0x20BB7) === String.fromCharCode(0x0BB7)
    , theChar, theChar.length, theChar.charCodeAt(0), theChar.charCodeAt(1));//11011000 01000010 : ‭11011111 10110111‬
console.log("theChar=" + theChar, "\u20BB7", "\u{20BB7}")
//ES6 新增 fromCodePoint和codePointAt来正确识别超过0xFFFF的字符
console.log(theChar === '𠮷', encodeURI('𠮷'), String.fromCodePoint(0x20BB7), '𠮷'.codePointAt(0));
/*
 记录一下笔记为什么对0x20BB7的拆分结果是0xD842, 0xDFB7

 首先需要知道UTF-8的编码格式：
 UTF-8是一种变长字节编码方式。对于某一个字符的UTF-8编码，如果只有一个字节则其最高二进制位为0；如果是多字节，其第一个字节从最高位开始，连续的二进制位值为1的个数决定了其编码的位数，其余各字节均以10开头。UTF-8最多可用到6个字节。
     如表：
     1字节 0xxxxxxx                                                 提供7个有效位
     2字节 110xxxxx 10xxxxxx                                        提供11个有效位
     3字节 1110xxxx 10xxxxxx 10xxxxxx                               提供16个有效位
     4字节 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx                      提供21个有效位
     5字节 111110xx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx             提供26个有效位
     6字节 1111110x 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx    提供31个有效位

 如果是单纯的对0x20BB7翻译成二进制是 ‭0010 00001011 10110111‬ 三个字节
 然后我们至少需要18个有效位来存放我们的这个汉字，
 检索UTF-8编码发现我们需要4个字节才能放入我们的这个汉子，提供21个有效位
 按照固定编码格式放入我们的这个汉字的位编码得到：
    11110-000|10-10 0000|10-1011 10|10-110111‬ =》‭F0A0AEB7‬ 这个是在网络传输中用的编码也就是encodeURI()得到的编码

然后上面的UTF-8编码并不是JavaScrip/Java采用的编码格式，准确的说，他们采用了UTF-16。
    小于等于0xFFFF的字符 
                            直接用0xFFFF 填充码点
    大于0xFFFF的字符需要把码点减去0x10000,然后再填充到下面两个UTF-16中，即32位
                            1101 10xx xxxxxxxx 1101 11xx xxxxxxxx
                            即第一个开头必须是1101 10,第二个开头必须是1101 11   提供20个有效位

回到我们最初的0x20BB7[‭0010 00001011 10110111],我们先减去 0x10000 得到 0x10BB7[‭0001 00001011 10110111]
然后把这个0x10BB7填入到20个有效位中得到
    1101 10-0001 000010 | 1101 11-11 10110111
    => D842 | DFB7 
到此为止我们已经完全理解JS中的编码规则了。
*/
//看下下面的实验例子:
console.log("测试码点UTF-16", String.fromCharCode(0xD800, 0xDC00), String.fromCharCode(0xD800), String.fromCharCode(0xDC00))
let testZ = '中';
for (let i = 0; i < testZ.length; i++) {
    console.log("testZ", testZ, testZ.charCodeAt(i).toString(16), testZ.codePointAt(0));
}
//实例属性
// String.prototype.length
/*实例方法
String.prototype.charAt()
String.prototype.charCodeAt()
String.prototype.concat()
String.prototype.slice()
String.prototype.substring()
String.prototype.substr()
String.prototype.indexOf()，String.prototype.lastIndexOf()
String.prototype.trim()
String.prototype.toLowerCase()，String.prototype.toUpperCase()
String.prototype.match()
String.prototype.search()，String.prototype.replace()
String.prototype.split()
String.prototype.localeCompare()
 */
var str = "123";
// 如果没有任何参数，charCodeAt返回首字符的 Unicode 码点
console.log("String对象 实例方法 ", str.length, str.charAt(0), str.charCodeAt(0), str.charCodeAt(), str.charCodeAt(-1));
// 注意，charCodeAt方法返回的 Unicode 码点不会大于65536（0xFFFF），
// 也就是说，只返回两个字节的字符的码点。如果遇到码点大于 65536 的字符（四个字节的字符），
// 必需连续使用两次charCodeAt，不仅读入charCodeAt(i)，还要读入charCodeAt(i+1)，
// 将两个值放在一起，才能得到准确的字符
console.log("中文长度", "中文".length, "ab".length, "中".charCodeAt(), String.fromCharCode(20013));
console.log("concat", str.concat("456", 7), str);//不改变源字符串
console.log("slice", str.slice(1, 7), str);//不改变源字符串
//start end
console.log("substring", str.substring(1, 2), str);//不改变源字符串
// 如果参数是负数，substring方法会自动将负数转为0
// 由于第二个参数小于第一个参数，会自动互换位置
// 由于这些规则违反直觉，因此不建议使用substring方法，应该优先使用slice
//start length
console.log("substr", str.substr(1, 1), str);//不改变源字符串
// 如果第一个参数是负数，表示倒数计算的字符位置。如果第二个参数是负数，将被自动转为0，因此会返回空字符串

console.log("indexOf", str.indexOf(1, 1), str.indexOf(1, 0), str);//不改变源字符串
console.log("lastIndexOf", str.lastIndexOf(1, 1), str.lastIndexOf(1, 0), str);//不改变源字符串
var str2 = " 空格 ]";
console.log("trim", str2.trim(), str2);//不改变源字符串
// 该方法去除的不仅是空格，还包括制表符（\t、\v）、换行符（\n）和回车符（\r）

str += "aBc";
console.log("toLowerCase", str.toLowerCase(), str);//不改变源字符串
console.log("toUpperCase", str.toUpperCase(), str);//不改变源字符串

var str3 = 'cat, bat, sat, fat2' // ["at"]
var matchs = str3.match("at")
//返回的数组还有index属性和input属性，分别表示匹配字符串开始的位置和原始字符串
console.log("match", matchs, matchs.input, matchs.index, str3.match("atx"), str3);
console.log("search", str3.search("at"), str3);
console.log("replace", str3.replace("at", "et"), str3);//默认只替换第一个
//替换全部参见正则表达式一章

console.log("split", str3.split(","), str3);
console.log("localeCompare", 'apple'.localeCompare('banana'), 'B'.localeCompare('a')
    , 'a'.localeCompare('a'), 'A'.localeCompare('a'));
// 该方法的最大特点，就是会考虑自然语言的顺序。举例来说，正常情况下，大写的英文字母小于小写字母
// localeCompare还可以有第二个参数，指定所使用的语言（默认是英语），然后根据该语言的规则进行比较

//Math对象
/*
Math.E：常数e。
Math.LN2：2 的自然对数。
Math.LN10：10 的自然对数。
Math.LOG2E：以 2 为底的e的对数。
Math.LOG10E：以 10 为底的e的对数。
Math.PI：常数π。
Math.SQRT1_2：0.5 的平方根。
Math.SQRT2：2 的平方根。

Math对象提供以下一些静态方法。
Math.abs()：绝对值
Math.ceil()：向上取整
Math.floor()：向下取整
Math.max()：最大值
Math.min()：最小值
Math.pow()：指数运算
Math.sqrt()：平方根
Math.log()：自然对数
Math.exp()：e的指数
Math.round()：四舍五入
Math.random()：随机数

Math.sin()：返回参数的正弦（参数为弧度值）
Math.cos()：返回参数的余弦（参数为弧度值）
Math.tan()：返回参数的正切（参数为弧度值）
Math.asin()：返回参数的反正弦（返回值为弧度值）
Math.acos()：返回参数的反余弦（返回值为弧度值）
Math.atan()：返回参数的反正切（返回值为弧度值）
*/

// Date 对象
// 它以1970年1月1日00:00:00作为时间的零点，可以表示的时间范围是前后各1亿天（单位为毫秒）
console.log("Date", Date(), Date(2000, 1, 1));
// 注意，即使带有参数，Date作为普通函数使用时，返回的还是当前时间
/*
年：使用四位数年份，比如2000。如果写成两位数或个位数，则加上1900，即10代表1910年。如果是负数，表示公元前。
月：0表示一月，依次类推，11表示12月。
日：1到31。
小时：0到23。
分钟：0到59。
秒：0到59
毫秒：0到999。
*/
console.log("new Date", new Date(2013, 0, 1, 0, 0, 0, 0), new Date(2013, 15));
// 注意，月份从0开始计算，但是，天数从1开始计算。另外，除了日期的默认值为1，小时、分钟、秒钟和毫秒的默认值都是0
// 这些参数如果超出了正常范围，会被自动折算。比如，如果月设为15，就折算为下一年的4月

// 两个日期实例对象进行减法运算时，返回的是它们间隔的毫秒数；进行加法运算时，返回的是两个字符串连接而成的新字符串
console.log("now", Date.now());
console.log("parse", Date.parse('Aug 9, 1995'));
console.log("parse", Date.parse('January 26, 2011 13:51:50'));
console.log("parse", Date.parse('Mon, 25 Dec 1995 13:30:00 GMT'));
console.log("parse", Date.parse('Mon, 25 Dec 1995 13:30:00 +0430'));
console.log("parse", Date.parse('2011-10-10'));
console.log("parse", Date.parse('2011-10-10T14:48:00'), Date.parse("xxx"), Date.UTC(2011, 0, 1, 2, 3, 4, 567));
// YYYY-MM-DDTHH:mm:ss.sssZ 其中最后的Z表示时区

/*
Date的实例对象，有几十个自己的方法，除了valueOf和toString，可以分为以下三类。
to类：从Date对象返回一个字符串，表示指定的时间。
get类：获取Date对象的日期和时间。
set类：设置Date对象的日期和时间

toString 返回一个完整的日期字符串
toUTCString 返回对应的 UTC 时间，也就是比北京时间晚8个小时
toISOString 返回对应时间的 ISO8601 写法
toJSON 返回一个符合 JSON 格式的 ISO 日期字符串，与toISOString方法的返回结果完全相同
toDateString 返回日期字符串（不含小时、分和秒）
toTimeString 返回时间字符串（不含年月日）

本地时间的字符串。
Date.prototype.toLocaleString()：完整的本地时间。
Date.prototype.toLocaleDateString()：本地日期（不含小时、分和秒）。
Date.prototype.toLocaleTimeString()：本地时间（不含年月日）

getTime()：返回实例距离1970年1月1日00:00:00的毫秒数，等同于valueOf方法。
getDate()：返回实例对象对应每个月的几号（从1开始）。
getDay()：返回星期几，星期日为0，星期一为1，以此类推。
getYear()：返回距离1900的年数。
getFullYear()：返回四位的年份。
getMonth()：返回月份（0表示1月，11表示12月）。
getHours()：返回小时（0-23）。
getMilliseconds()：返回毫秒（0-999）。
getMinutes()：返回分钟（0-59）。
getSeconds()：返回秒（0-59）。
getTimezoneOffset()：返回当前时间与 UTC 的时区差异，以分钟表示，返回结果考虑到了夏令时因素。
    分钟和秒：0 到 59
    小时：0 到 23
    星期：0（星期天）到 6（星期六）
    日期：1 到 31
    月份：0（一月）到 11（十二月）
    年份：距离1900年的年数

//UTC版本
getUTCDate()
getUTCFullYear()
getUTCMonth()
getUTCDay()
getUTCHours()
getUTCMinutes()
getUTCSeconds()
getUTCMilliseconds()

setDate(date)：设置实例对象对应的每个月的几号（1-31），返回改变后毫秒时间戳。
setYear(year): 设置距离1900年的年数。
setFullYear(year [, month, date])：设置四位年份。
setHours(hour [, min, sec, ms])：设置小时（0-23）。
setMilliseconds()：设置毫秒（0-999）。
setMinutes(min [, sec, ms])：设置分钟（0-59）。
setMonth(month [, date])：设置月份（0-11）。
setSeconds(sec [, ms])：设置秒（0-59）。
setTime(milliseconds)：设置毫秒时间戳

//UTC版本
setUTCDate()
setUTCFullYear()
setUTCHours()
setUTCMilliseconds()
setUTCMinutes()
setUTCMonth()
setUTCSeconds()
*/

// RegExp对象
// 新建正则表达式有两种方法。一种是使用字面量，以斜杠表示开始和结束。
// var regex = /xyz/;
// 另一种是使用RegExp构造函数。
// var regex = new RegExp('xyz');
// 前者的效率较高。而且，前者比较便利和直观，所以实际应用中，基本上都采用字面量定义正则表达式

// 一类是修饰符相关，返回一个布尔值，表示对应的修饰符是否设置。
// RegExp.prototype.ignoreCase：返回一个布尔值，表示是否设置了i修饰符。
// RegExp.prototype.global：返回一个布尔值，表示是否设置了g修饰符。
// RegExp.prototype.multiline：返回一个布尔值，表示是否设置了m修饰符
// RegExp.prototype.lastIndex：返回一个整数，表示下一次开始搜索的位置。该属性可读写，但是只在进行连续搜索时有意义，详细介绍请看后文。
// RegExp.prototype.source：返回正则表达式的字符串形式（不包括反斜杠），该属性只读。
// RegExp.prototype.test() 正则实例对象的test方法返回一个布尔值，表示当前模式是否能匹配参数字符串
// 如果正则表达式带有g修饰符，则每一次test方法都从上一次结束的位置开始向后匹配
// 带有g修饰符时，可以通过正则对象的lastIndex属性指定开始搜索的位置
// 如果正则模式是一个空字符串，则匹配所有字符串
// RegExp.prototype.exec()
var s = '_x_x';
var r1 = /x/;
var r2 = /y/;
console.log("exec", r1.exec(s), r2.exec(s), /_(x)/.exec(s));
// 如果正则表示式包含圆括号（即含有“组匹配”），则返回的数组会包括多个成员。
// 第一个成员是整个匹配成功的结果，后面的成员就是圆括号对应的匹配成功的组。
// 也就是说，第二个成员对应第一个括号，第三个成员对应第二个括号，以此类推。整个数组的length属性等于组匹配的数量再加1
// 结果带属性 
// input：整个原字符串。
// index：整个模式匹配成功的开始位置（从0开始计数）

// 正则实例对象的lastIndex属性不仅可读，还可写。设置了g修饰符的时候，只要手动设置了lastIndex的值，就会从指定位置开始匹配

var s = 'abba';
var r = /a/g;
console.log("字符串match和exec", s.match(r), r.exec(s));//match会一次性返回所有匹配成功的结果

/*
replace方法的第二个参数可以使用美元符号$，用来指代所替换的内容。
$&：匹配的子字符串。
$`：匹配结果前面的文本。
$'：匹配结果后面的文本。
$n：匹配成功的第n组内容，n是从1开始的自然数。
$$：指代美元符号$。
*/
console.log("replace", 'hello world'.replace(/(\w+)\s(\w+)/, '$2 $1'), 'abc'.replace('b', '[$`-$&-$\']'));
// replace方法的第二个参数还可以是一个函数，将每一个匹配内容替换为函数返回值
console.log("replace", '3 and 5'.replace(/[0-9]+/g, function (match, pos, src) {
    console.log("function", match, "|", pos, "|", src);
    return 2 * match;
}));
// 作为replace方法第二个参数的替换函数，可以接受多个参数。
// 其中，第一个参数是捕捉到的内容，第二个参数是捕捉到的组匹配（有多少个组匹配，就有多少个对应的参数）。
// 组匹配需要用小括号()
// 此外，最后还可以添加两个参数，倒数第二个参数是捕捉到的内容在整个字符串中的位置（比如从第五个位置开始），
// 最后一个参数是原字符串

// String.prototype.split()
// 字符串对象的split方法按照正则规则分割字符串，返回一个由分割后的各个部分组成的数组。

// 匹配规则
/*
字面量字符和元字符
    1）点字符（.)
        匹配除回车（\r）、换行(\n) 、行分隔符（\u2028）和段分隔符（\u2029）以外的所有字符。
        注意，对于码点大于0xFFFF字符，点字符不能正确匹配，会认为这是两个字符
    2）位置字符
        位置字符用来提示字符所处的位置，主要有两个字符。
        ^ 表示字符串的开始位置
        $ 表示字符串的结束位置
    3）选择符（|）
        竖线符号（|）在正则表达式中表示“或关系”（OR），即cat|dog表示匹配cat或dog

转义符
    正则表达式中那些有特殊含义的元字符，如果要匹配它们本身，就需要在它们前面要加上反斜杠。比如要匹配+，就要写成\+

特殊字符
    正则表达式对一些不能打印的特殊字符，提供了表达方法。
    \cX 表示Ctrl-[X]，其中的X是A-Z之中任一个英文字母，用来匹配控制字符。
    [\b] 匹配退格键(U+0008)，不要与\b混淆。
    \n 匹配换行键。
    \r 匹配回车键。
    \t 匹配制表符 tab（U+0009）。
    \v 匹配垂直制表符（U+000B）。
    \f 匹配换页符（U+000C）。
    \0 匹配null字符（U+0000）。
    \xhh 匹配一个以两位十六进制数（\x00-\xFF）表示的字符。
    \uhhhh 匹配一个以四位十六进制数（\u0000-\uFFFF）表示的 Unicode 字符

字符类
    所有可供选择的字符都放在方括号内，比如[xyz] 表示x、y、z之中任选一个匹配
    字符类（class）表示有一系列字符可供选择，只要匹配其中一个就可以了。

    1）脱字符（^）
        如果方括号内的第一个字符是[^]，则表示除了字符类之中的字符，其他字符都可以匹配。
        比如，[^xyz]表示除了x、y、z之外都可以匹配
    2）连字符（-）
        某些情况下，对于连续序列的字符，连字符（-）用来提供简写形式，表示字符的连续范围。
        比如，[abc]可以写成[a-c]，[0123456789]可以写成[0-9]，同理[A-Z]表示26个大写字母

预定义模式
    预定义模式指的是某些常见模式的简写方式。
    \d 匹配0-9之间的任一数字，相当于[0-9]。
    \D 匹配所有0-9以外的字符，相当于[^0-9]。
    \w 匹配任意的字母、数字和下划线，相当于[A-Za-z0-9_]。
    \W 除所有字母、数字和下划线以外的字符，相当于[^A-Za-z0-9_]。
    \s 匹配空格（包括换行符、制表符、空格符等），相等于[ \t\r\n\v\f]。
    \S 匹配非空格的字符，相当于[^ \t\r\n\v\f]。
    \b 匹配词的边界。
    \B 匹配非词边界，即在词的内部

重复类
    模式的精确匹配次数，使用大括号（{}）表示。{n}表示恰好重复n次，{n,}表示至少重复n次，{n,m}表示重复不少于n次，不多于m次

量词符
    量词符用来设定某个模式出现的次数。
    ? 问号表示某个模式出现0次或1次，等同于{0, 1}。
    * 星号表示某个模式出现0次或多次，等同于{0,}。
    + 加号表示某个模式出现1次或多次，等同于{1,}

贪婪模式
    上一小节的三个量词符，默认情况下都是最大可能匹配，即匹配直到下一个字符不满足匹配规则为止。这被称为贪婪模式

    除了非贪婪模式的加号，还有非贪婪模式的星号（*）和非贪婪模式的问号（?）。
    +?：表示某个模式出现1次或多次，匹配时采用非贪婪模式。
    *?：表示某个模式出现0次或多次，匹配时采用非贪婪模式。
    ??：表格某个模式出现0次或1次，匹配时采用非贪婪模式

修饰符
    修饰符（modifier）表示模式的附加规则，放在正则模式的最尾部。
    修饰符可以单个使用，也可以多个一起使用

    1）g 修饰符
        默认情况下，第一次匹配成功后，正则对象就停止向下匹配了。g修饰符表示全局匹配（global），
        加上它以后，正则对象将匹配全部符合条件的结果，主要用于搜索和替换
    2）i 修饰符
        默认情况下，正则对象区分字母的大小写，加上i修饰符以后表示忽略大小写（ignorecase）
    3）m 修饰符
        m修饰符表示多行模式（multiline），会修改^和$的行为。默认情况下（即不加m修饰符时），
        ^和$匹配字符串的开始处和结尾处，加上m修饰符以后，^和$还会匹配行首和行尾，即^和$会识别换行符（\n）

组匹配
    1）概述
        正则表达式的括号表示分组匹配，括号中的模式可以用来匹配分组的内容
            /fred+/.test('fredd') // true
            /(fred)+/.test('fredfred') // true
        上面代码中，第一个模式没有括号，结果+只表示重复字母d，第二个模式有括号，结果+就表示匹配fred这个词

        正则表达式内部，还可以用\n引用括号匹配的内容，n是从1开始的自然数，表示对应顺序的括号
        括号还可以嵌套
            /y((..)\2)\1/.test('yabababab') // true
            上面代码中，\1指向外层括号，\2指向内层括号
    2）非捕获组
        (?:x)称为非捕获组（Non-capturing group），表示不返回该组匹配的内容，即匹配的结果中不计入这个括号
            var m = 'abc'.match(/(?:.)b(.)/);
            m // ["abc", "c"]
            上面代码中的模式，一共使用了两个括号。其中第一个括号是非捕获组，
            所以最后返回的结果中没有第一个括号，只有第二个括号匹配的内容
    3）先行断言
        x(?=y)称为先行断言（Positive look-ahead），x只有在y前面才匹配，y不会被计入返回结果。
        比如，要匹配后面跟着百分号的数字，可以写成/\d+(?=%)/
    4）先行否定断言
        x(?!y)称为先行否定断言（Negative look-ahead），x只有不在y前面才匹配，y不会被计入返回结果。
        比如，要匹配后面跟的不是百分号的数字，就要写成/\d+(?!%)/
*/
console.log("组匹配", /y(..)(.)\2\1/.test('yabccab'), /y((..)\2)\1/.test('yabababab'));
console.log("组匹配", /(.)b(.)/.exec("abc"), /(?:.)b(.)/.exec("abc"));

/**
 * JSON对象
 * 
 * JSON 对值的类型和格式有严格的规定。
 * 
 * 1.复合类型的值只能是数组或对象，不能是函数、正则表达式对象、日期对象。
 * 2.原始类型的值只有四种：字符串、数值（必须以十进制表示）、布尔值和null（不能使用NaN, Infinity, -Infinity和undefined）。
 * 3.字符串必须使用双引号表示，不能使用单引号。
 * 4.对象的键名必须放在双引号里面。
 * 5.数组或对象最后一个成员的后面，不能加逗号
 */

//JSON.stringify()
//JSON.stringify方法用于将一个值转为 JSON 字符串。该字符串符合 JSON 格式，并且可以被JSON.parse方法还原
console.log("JSON对象 stringify", JSON.stringify(true), JSON.stringify('true'), JSON.stringify(/foo/));
// JSON.stringify方法会忽略对象的不可遍历的属性
var obj = {};
Object.defineProperties(obj, {
    'foo': {
        value: 1,
        enumerable: true
    },
    'bar': {
        value: 2,
        enumerable: false
    }
});
console.log(JSON.stringify(obj)); // "{"foo":1}"
// JSON.stringify方法还可以接受一个数组，作为第二个参数，指定需要转成字符串的属性
// 这个类似白名单的数组，只对对象的属性有效，对数组无效
// 第二个参数还可以是一个函数，用来更改JSON.stringify的返回值
function f(key, value) {//上面代码中的f函数，接受两个参数，分别是被转换的对象的键名和键值
    if (typeof value === "number") {
        value = 2 * value;
    }
    console.log("JSON.stringify 函数", key, value);
    return value;
}

console.log("JSON.stringify,第二个参数是数组", JSON.stringify({ a: 1, b: 2 }, ["a"]));
//node 环境只返回一个 {} ,并没有调用传入的f函数
console.log("JSON.stringify,第二个参数是函数", JSON.stringify({ a: 1, b: 2 }, f));
// 第三个参数 用于增加可读性
console.log("JSON.stringify,第三个参数是 可读性空格或前缀", JSON.stringify({ a: 1, b: 2 }, null, "value = "));
// 参数对象的toJSON方法
var user = {
    firstName: '三',
    lastName: '张',

    get fullName() {
        return this.lastName + this.firstName;
    },

    toJSON: function () {
        return {
            name: this.lastName + this.firstName
        };
    }
};
console.log(JSON.stringify(user));

// JSON.parse()
// JSON.parse方法用于将 JSON 字符串转换成对应的值
console.log("", JSON.parse('{"name": "张三"}'));
// 如果传入的字符串不是有效的 JSON 格式，JSON.parse方法将报错。
// JSON.parse方法可以接受一个处理函数，作为第二个参数，用法与JSON.stringify方法类似
