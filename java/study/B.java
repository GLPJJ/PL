package study;

public class B {
    public static void main(String[] args) {
        // if语句
        if (true)
            System.out.println("1 is true");

        // if-else if-else 语句
        int r = 3;
        if (r == 1) {
            // 后跟一个语句块
            System.out.println("r is 1");
        } else if (r == 2)
            System.out.println("r is 2");
        else if (r == 3) {
            System.out.println("r is 3");
        } else {
            System.out.println("r is not in (1,2,3)");
        }

        // 默认情况，同样的判读语句，switch语句的执行效率会更高。
        // switch 语句
        switch (r) {
            case 1:
                System.out.println("switch r is 1");
                break;
            case 2:
                System.out.println("switch r is 2");
                break;
            case 3:
                System.out.println("switch r is 3");
                // break;这里如果不加break，后面的case和default的语句也会执行。 go语言的话默认不需要break。
            default:
                System.out.println("switch r is not in (1,2,3)");
        }

        // 循环语句
        for (int i = 0; i < 5; i++) {
            System.out.println("for " + i);
        }
        for (int i = 0, j = 5; i < j; i++) {
            if (i == 1)
                continue;
            if (i == 3)
                break;//return;
            System.out.println("for2 " + i + "," + j);
        }

        int i = 0;
        while (i < 5) {
            System.out.println("while " + i);
            i++;
        }

        do {
            System.out.println("do " + i);
            i++;
        } while (i < 5);
    }
}
