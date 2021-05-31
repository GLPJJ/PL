interface UserBase {
    flag: boolean;//布尔值

    //Boolean 大写表示类/接口，小写表示基础数据类型
}

declare class DllCls {//导出类
    init(flag: boolean): boolean;//声明函数
};

// class DllCls{
//     init(flag:boolean):boolean{
//         return true;
//     }
// }

// namespace Test{
//     enum Color {Red, Green, Blue };
// }

enum Color { Red, Green, Blue };

class UserData implements UserBase {
    flag: boolean;//基础数据类型

    score: number;//数字
    name: string;//字符串

    //phone?: String; //？ 表示初始化可为空 tsc 编译失败

    list1: number[];//数组
    list2: Array<number>;//数组

    tuple1: [string, number];//元组

    any1: any;//任意值，这样可以访问现在还未指定方法

    object1: Object;//对象，只能指定对象

    list3: any[] = [1, "2", true]

    //void //指定不返回
    //undefined //未定义
    //null      //空值

    //断言 as
    someValue: any = "this is a string";
    //strLength: number = (this.someValue as string).length; // 并不能用

    constructor() {
        console.log("constructor UserData");

        /**
         * let比var多了
         *  作用域之外销毁的功能
         *  屏蔽重定义
         *  块级作用域变量的获取
         * 
         * 不过我们尽量少用屏蔽功能，否则容易看不懂代码
         */
        let temp1 = true;//变量赋值，
        const temp2 = 1;//常量赋值

        //解构数组
        let arra = [1, 2];
        let [first, second] = arra;
        console.log("解构数组:" + first + "," + second);

        try {
            throw "oh no!";
        }
        catch (e) {
            console.log("Oh well.");
        }

    }
}

class UserMath extends UserData {

    math: Number;
    static cls: string = "数学";
    //readonly cls_type:number = 1;//tsc 编译成js 报错？？？

    constructor() {//构造函数
        super();
        console.log("constructor UserMath");
    }

    public getMath(add: Number): number {//返回值
        let temp = this.flag ? add.valueOf() : 0;//三目运算符
        return this.math.valueOf() + temp;
    }

    /**
     * getLevel
     */
    public getLevel(): String {
        if (this.math >= 90)
            return "优秀";
        else if (this.math >= 75)
            return "良";
        else if (this.math >= 60)
            return "及格";
        else
            return "不及格";
    }

    /**
     * getPP
     */
    public getPP(): String {
        switch (this.getLevel()) {
            case "优秀":
                return "好";
            default:
                return "不好";
        }
    }
}

for (let i = 0; i < 10; i++) {
    console.log("console1:" + i);
}

let j = 0;
while (j < 10) {
    console.log("console2:" + j);
    j++;
}

let objTs = new UserMath();

