package study;

public class D {

    // 申明本函数抛出异常。，可以是多个异常，以逗号分隔
    public static void testException() throws MyException {
        // int a = 5 / 0;//除数是0
        throw new MyException("argument error");// 自己主动抛出异常
    }

    // 自定义异常,如果不声明static，则不能再static的testException方法中创建。
    static class MyException extends Exception {

        /**
         *
         */
        private static final long serialVersionUID = 1L;

        public MyException(String err) {
            super("MyException:" + err);
        }
    }

    public static void main(String[] args) {// args代表程序启动的命令行参数
        // 字符串对象常用方法,java的字符串也是一个String对象，该对象相对于变量来说是不可改变的，如果想要改变可以使用StringBuffer
        String str = "hello 世界  ";// 双引号表示字符串，单引号表示字符 char
        System.out.println("str.length 字符串长度=" + str.length());
        System.out.println("str charAt(0)=" + str.charAt(0) + ",charAt(6)=" + str.charAt(6));

        String str2 = "hello 世界";
        // 常量字符串对象地址也一样。
        System.out.println("str.length 字符串比较=" + str.equals(str2) + ",字符串对象比较=" + (str == str2));
        String str3 = new StringBuffer().append("hello").append(" 世界").toString();
        // 变量地址与常量字符串地址不一致。
        System.out.println("str.length 字符串比较=" + str.equals(str3) + ",字符串对象比较=" + (str == str3));

        // charAt 获取某个索引char
        // equals,equalsIgnoreCase 比较，忽略大小写比较
        // indexOf,lastIndexOf 查找字符串
        System.out.println("indexOf=" + str.indexOf("l") + ",lastIndexOf=" + str.lastIndexOf("l"));

        // startsWith,endsWith 前缀，后缀
        System.out.println("startsWith=" + str.startsWith("世界") + ",endsWith=" + str.endsWith("世界"));
        // compareTo >0 比传入的大，=0 相等，<0 比传入的小 字符串比较大小
        System.out.println("compareTo=" + str.compareTo("世界"));

        // 下面的函数操作不会更改原来字符串对象的值
        // substring 前闭后开区间。取子串
        System.out.println("substring=" + str.substring(1, 7) + ",origin str=" + str);
        // concat拼接字符串，功能等同于 +
        System.out.println("concat=" + str.concat(",中guo") + ",origin str=" + str);
        // replace替换所有
        System.out.println("replace=" + str.replace("l", "L") + ",origin str=" + str);
        // trim 删除字符串前后的空白部分
        System.out.println("trim=" + str.trim() + ",origin str=" + str);

        // valueOf 转字符串。String.valueOf();

        System.out.println("toUpperCase=" + str.toUpperCase() + ",origin str=" + str);
        System.out.println("toLowerCase=" + str.toLowerCase() + ",origin str=" + str);

        String[] strs = { "hello", "世界" };
        for (int i = 0; i < strs.length; i++) {
            System.out.println("strs[" + i + "]=" + strs[i]);
        }

        System.out.println("args begin len=" + args.length);
        for (int i = 0; i < args.length; i++) {
            System.out.println("args[" + i + "]=" + args[i]);
        }
        System.out.println("args end");

        // StringBuffer charAt setCharAt reverse
        StringBuffer sb = new StringBuffer();
        sb.append("check").append('=').append(10);
        System.out.println("StringBuffer append=" + sb.toString());
        sb.insert(0, "gg");
        System.out.println("StringBuffer insert=" + sb.toString());
        sb.reverse();
        System.out.println("StringBuffer reverse=" + sb.toString());
        sb.delete(0, 1);
        sb.deleteCharAt(5);
        System.out.println("StringBuffer delete=" + sb.toString());
        sb.replace(0, 1, "aa");
        System.out.println("StringBuffer replace=" + sb.toString());
        System.out.println("StringBuffer substring=" + sb.substring(5));
        // 如果ctrl+alt+左 快捷键失灵，开始菜单搜显卡，打开快捷键设置，设置然后关闭，即可解决。

        // 对应的简单类型，提供一个类的封装
        // byte->Byte short->Short int->Integer long->Long
        // float->Float double->Double
        // boolean->Boolean
        // char->Character
        // void->Void
        // 字符串转数字
        System.out.println("转换数字=" + Integer.parseInt("123", 10) + ",小数=" + Double.parseDouble("2.6"));

        System.out.println("时间戳(毫秒)：" + System.currentTimeMillis());
        // System.arraycopy() 速度要比简单的数组拷贝快

        // 捕获异常
        try {
            testException();
        } catch (Exception e) {
            e.printStackTrace();
            return;// 这里的return只会影响 try catch exception end 的打印，finally语句内容还是会执行。
        } finally {
            System.out.println("try catch exception finally");
        }
        System.out.println("try catch exception end");
    }
}
