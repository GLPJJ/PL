package study;//包名，使用关键字package。其实就是所在目录,本类A的全称是study.A

//java 由于广泛的使用，所以常见的IDE对引入包已经非常方便 import

//单行注释

/*
 * 多行注释
 * 
 * 在编译之前我们需要把当前目录定位到study目录，然后才能执行。否则会提示找不到文件的类似错误
 * 1.编译java文件 
 * 编译指令: cd java 目录 javac -encoding utf8 study/A.java 
 * 2.运行java
 * java study.A
 * 
 */

/*
 * java基础数据
 * 整数型：byte，short，int，long     
 *      0888表示8进制，0x888表示16进制，通常888表示10进制  888l(或者L)表示使用long型表示，默认int
 * 浮点型：float，double
 *      小数默认使用double，使用0.156f(或者F)强制使用float表示。  E或者e表示10的幂  1.2E10，1.3e-10。
 * 字符型：char                     
 *      java中的char与c语言不同，表示的是unicode码，16位表示。
 *      转义序列                    说明     
 *      \ddd                    八进制字符
 *      \ uxxxx                 十六进制Unicode码字符
 *      \' \" \\                单引号，双引号，反斜杠
 *      \r \n \f \t \b          回车，换行，换页，水平制表符，退格
 * 
 *      java中的字符串只能在同一行开始和结束，没有换行连接符。
 *      而且java中的字符串实际实现是一个类，不像c语言是字符数组。
 * 布尔型：boolean
 *      true，false
 * 
 * java拥有严格的变量作用域，内部域可以访问外部域的数据，反过来就会报错。
 * {
 *      int a = 10;//变量必须先申明再使用。
 *      a++;
 *      {
 *          int b = 20;
 *          //这里不能再使用a申请新的变量。  c语言可以。
 *      }
 *      //b属于内部域，这里无法使用。
 * }
 * 
 */

class A {// 类名与文件名大小保持一致。
    public static void main(String[] args) {
        System.out.println("Hello 世界");

        System.out.println("强制类型转换 (byte)257=" + ((byte) 257));// 相当于 x%256取余数。
        System.out.println("强制类型转换 (int)1.2=" + ((int) 1.2));// 相当于 舍弃小数部分
        // 在表达式中，java执行自动类型提升，把byte和short提升到int再计算表达式的值。
        byte x, y;
        x = 40;
        y = 50;
        int z = x * y;// 表达式自动提升,如果有更大的数据类型，那就继续提升直至double
        System.out.println("表达式自动提升类型计算z=" + z);//

        // 数组的申明和使用，数组下标同c语言一样，从0开始。
        // 一维数组
        int arra[] = new int[6];// 分配动态内存，并初始化为0
        int brra[] = { 1, 2, 3, 4, 5, 6 };
        System.out.println("数组arra[0]=" + arra[0] + ",brra[5]=" + brra[5]);
        // 多维数组
        int[][] aarra = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 } };
        System.out.println("多维数组 aarra[0][2]=" + aarra[0][2]);

        // 1.算术运算符:
        int a = 10;
        int b = 20;
        System.out.println("a+b=" + (a + b)); // 加
        System.out.println("'11'+b=" + ("11" + b));// 对字符串操作，就是拼接。
        System.out.println("a-b=" + (a - b)); // 减
        System.out.println("a*b=" + (a * b)); // 乘
        System.out.println("b/a=" + (b / a)); // 除 java同c语言一样舍弃余数。
        System.out.println("b%a=" + (b % a)); // 模 java取模可用于小数，c语言只能用于整数
        System.out.println("b^a=" + Math.pow(a, b)); // 指数，使用Math方法
        System.out.println("-a=" + -a);
        // += -= *= /= %= 都可以表示为 a=a+x。对自身运算后再赋值给自身。
        System.out.println("-a=" + (a++));// 自加1 a++表示先返回自加1，++a表示先自加1再返回
        System.out.println("-a=" + (a--));// 自减1 同理++
        System.out.println("*********************************");

        // 2.比较操作符: 短路运算规则！，运算符优先级如果不清楚，可以增加圆括号，这样的增加不会影响执行效率。
        System.out.println("a==b " + (a == b));
        System.out.println("a!=b " + (a != b)); // 这个区别与别的 !=
        System.out.println("a>b " + (a > b));
        System.out.println("a<b " + (a < b));
        System.out.println("a>=b " + (a >= b));
        System.out.println("a<=b " + (a <= b));
        System.out.println("a<=b " + (a <= b ? "true" : "false"));// 三目运算符

        // a += 2 lua中没有这样的赋值运算符，需要自己写成 a = a+2

        // 3.逻辑运算符:
        boolean a1 = true; // 这里必须小写
        boolean b1 = false;
        System.out.println(a1 && b1);
        System.out.println(a1 || b1);
        System.out.println(!a1);

        // 4.位运算符：
        int a2 = 3; // 二进制的表示 0000 0011
        int b2 = 10; // 二进制的表示 0000 1010
        System.out.println("a&b =" + (a2 & b2)); // 按位与
        System.out.println("a|b =" + (a2 | b2)); // 按位或
        System.out.println("a^b =" + (a2 ^ b2)); // 按位异或
        System.out.println("~b =" + ~b2); // 按位取反
        System.out.println("a<<2 =" + (a2 << 2)); // 按位左移
        System.out.println("b>>2 =" + (b2 >> 2)); // 按位右移 左边空出的位置用符号位填充
        System.out.println("b>>>2 =" + (b2 >>> 2)); // 按位右移 左边空出的位置用0填充

        byte by = (byte) 0xf1;
        byte by1 = (byte) 0x11;
        short sh = (short) 0xfff2;
        short sh1 = (short) 0xf2;
        // java中没有无符号的类型，所以btye转int的时候，空的位置根据符号位来填充，如果最高位是1，则空位全部填1，否则填0
        System.out.printf("by = %x,%x\n", by, (int) by);
        System.out.printf("by1 = %x,%x\n", by1, (int) by1);
        System.out.printf("sh = %x,%x\n", sh, (int) sh);
        System.out.printf("sh1 = %x,%x\n", sh1, (int) sh1);
        System.out.printf("(by >> 4) = %x\n", (by >> 4));
        System.out.printf("(byte) (by >> 4) = %x\n", (byte) (by >> 4));
        System.out.printf("(byte) (by >>> 4) = %x\n", (byte) (by >>> 4));

        // 字符串数字转换
        System.out.println("字符串->数字:" + Integer.parseInt("1"));
        System.out.println("数字->字符串:" + 1);// 字符串+数字 就会转换成字符串
    }
}
