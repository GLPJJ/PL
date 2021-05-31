package study;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;

//输入输出
public class F {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("请输入（stop回车终止）：");
        while (!br.readLine().equals("stop")) {
        }

        System.out.println("end");

        if (args.length >= 2) {
            FileInputStream fis = new FileInputStream(args[0]);
            FileOutputStream fos = null;
            try {
                fos = new FileOutputStream(args[1]);
                int read;
                while ((read = fis.read()) != -1) {
                    fos.write(read);
                }
            } catch (Exception e) {
            } finally {
                if (fis != null)
                    fis.close();
                if (fos != null)
                    fos.close();
            }

        }

        // transient 关键字表示该变量不需要维持。
        // volatile 关键字表示该变量可以被程序的其他部分改变。
        // c语言表示总是从内存读取数据，不能只读取寄存器中的变量。

        // 使用instanceof 判断某个对象是否是某个类的实例，可以强制转化
        System.out.println("br instanceof Reader:" + (br instanceof Reader));

        // strictfp => strict float point 使用标准浮点数计算。
    }

    // 本机方法，c语言实现的方法。
    public static native String NativeHello();
    //javac -encoding utf8 study/F.java
    //javah -encoding utf8 -jni study.F 生成对应的NativeHello的C方法。
}
