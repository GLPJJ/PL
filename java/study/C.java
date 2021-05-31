package study;

//java没有独立的函数，所有的函数都在类中。所以我们这里就开始做类+函数的测试了。

interface Area {// 定义接口
    // 定义接口方法，计算面积返回double类型,方法名是calcS，()表示不需要传递参数
    double calcS();
}

// 相比于interface，还可以使用abstract来表明一个虚类，只实现部分方法
// 接口也可以继承
interface ZhouChang extends Area {
    double zhouchagn();// 计算周长
}

// 如果一个类只有局部实现接口，那么必须定义为abstract类。
class Rectangle implements Area {// 定义矩形实现接口
    // java中的访问权限多了一个默认访问权限！
    // 封装，同一个类中可见，其他都不可见。
    private double h;// 成员变量-高
    // 默认访问权限,同一个类中可见，同一个包的子类、非子类可以访问。
    double alpha;// 成员变量透明度
    // 封装，同一个类中可见，同一个包的子类、非子类可以访问，非同一包的子类可以访问
    protected double w;// 成员变量-宽

    // public都可以访问，无限制。
    // 公开的构造方法。构造方法函数名与类名保持一致。构造函数没有返回类型，其实默认是返回自己类的类型。
    public Rectangle(double w, double h) {
        // 这里的this关键字代表自身实例
        // 相对于类空间，构造函数空间范围更小，直接写w是指传进来的参数w，它将覆盖类空间的w。
        // 所以我们需要用this来特意指定类空间的w
        this.w = w;// 简单数据都是直接值拷贝的，对象都是拷贝引用，也即是值拷贝和引用拷贝的区别。
        this.h = h;

        // 值拷贝(call-by-value)的话，修改数据不改变原来的值
        // 引用拷贝(call-by-reference)的话，修改数据会改变原来的值
    }

    /*
     * 如果没有申明构造函数，java会创建一个默认构造函数,类似下面这个
     * 
     * public Rectangle(){//如果申明，也是可以的，就是构造函数重载。
     * 
     * }
     */

    @Override
    protected void finalize() {
        // java使用垃圾回收机制，当一个对象没有引用的时候，就会触发回收机制，如果在该对象被回收前需要释放一些资源，
        // 我们可以放到这个函数里实现。

        // 该函数与c语言的析构函数不一致，c语言的析构函数在出作用域的时候回执行，而java的finalize则不能确定什么时候执行。
    }

    @Override
    public double calcS() {// 接口实现。
        return this.w * this.h;// 用return 返回需要的值
    }

    public double getW() {
        return w;
    }

    // void表示不返回
    public void setW(double w) {
        this.w = w;
    }

    // 在同一个类里面允许有同名的方法，参数不一致。我们称为重载(overloaded)。方法重载。
    // 重载方法必须要有参数上的区别，可以是数量也可使是类型
    public void setW(double w, double h) {
        this.w = w;
        this.h = h;
    }

    public int getOverload() {
        return 0;
    }

    public int getOverload(double a) {
        return 1;
    }

    // 传递类引用。引用拷贝
    public boolean equal(Rectangle a) {
        return this.w == a.w && this.h == a.h;
    }

    public void callByValue(int a) {
        a += 100;
    }

    public void callByReference(Rectangle a) {
        a.w += 10;
    }

    public void show() {
        System.out.println("show Rectangle");
    }
}

// java不支持继承多个超类superclass,但是支持实现多个接口interface
// c语言支持继承多个超类。
class Square extends Rectangle {// 定义正方形继承矩形
    Square(double w) {// 构造方法
        // super表示调用父类构造方法。
        super(w, w);// 正方形就是宽跟高一样的矩形，该语句必须是子类构造函数的第一句。

        // 使用super可以访问超类(父类)的成员变量和成员方法。
        System.out.println("super.w=" + super.w + ",super.getW()=" + super.getW());

        // 一系列继承类的构造函数执行顺序是先执行超类构造，然后依次执行子类构造。
        // 如果是C语言的话，析构函数的执行顺序是先子类析构，然后依次执行超类(父类)析构
    }

    public Square makeSquare(double w) {
        Square ret = new Square(w);// 因为是new，动态分配的对象，不用担心被回收。
        return ret;
    }

    // 递归。
    public void recursion(int a) {
        if (a == 0) {
            return;
        }
        System.out.println("recursion a =" + a);
        recursion(a - 1);
    }

    // 方法覆盖：子类覆盖超类方法，需要方法名和参数都一致。如果参数不一致那么只是方法重载
    public void show() {
        System.out.println("show Square");

        // 父类的方法被隐藏，如果想要继续执行可以使用super
        // super.show();
    }
}

// final关键字阻止继承，表示他是一个最终类，不允许有继承。
// 默认的Object类，所有的java对象都是Object的子类。
final class Circle implements Area {// 定义圆实现接口
    // 封装，默认private
    private double r;// 成员变量-半径

    Circle(double r) {// 构造方法
        this.r = r;
    }

    @Override
    public double calcS() {// 实现圆的面积计算。
        return Circle.GetPi() * r * r;
    }

    // 关键字static修饰的类变量。关键字final 这里的用法类似于c语言的const，表示不能再改变。
    public static final double PI = 3.1415926;

    // 关键字static表示该方法不是实例方法，属于类方法,不用创建实例就能调用。一般不带static的方法都是成员方法。
    // 使用关键字final表示该方法不能重载
    public static final double GetPi() {
        // static函数体也没有this。只能访问类变量。
        return PI;
    }

    // static 语句块，表示类加载的时候执行，而且仅执行一次。
    static {
        System.out.println("Circle is loaded");
    }

    class Inner {// 内部类
        void deal() {
            System.out.println("call Inner r=" + r);// 内部类可以直接访问外部类的成员属性方法，反之不行
        }
    }

    static class InnerS {// 静态内部类
        void deal(double r) {
            System.out.println("call InnerS r=" + r);// 静态内部类不可以直接访问外部类的成员属性方法
        }
    }

    public void testInner() {
        Inner a = new Inner();
        a.deal();

        InnerS b = new InnerS();
        b.deal(r);
    }
}

public class C {// 定义公开类，跟文件名保持大小写一致。
    public static void main(String[] args) {
        Rectangle rect = new Rectangle(200, 100);// 创建一个矩形实例
        System.out.println("rect area=" + rect.calcS());// 计算面积
        System.out.println("rect alpha=" + rect.alpha);// 计算面积

        Square squre = new Square(100);// 创建一个正方形实例，每个实例的成员变量或者说属性都是独立的。
        System.out.println("squre area=" + squre.calcS());// 计算面积

        // rect.w 属性私有，无法直接访问。
        System.out.println("rect w=" + rect.getW() + ",squre w=" + squre.getW());// 两个属性独立

        Rectangle rect2 = rect;// 复制引用，这里没有创建新的实例！
        rect2.setW(150);// 修改引用的值会修改原值
        System.out.println("rect area=" + rect.calcS());// 计算面积

        // getOverload 并没有提供int参数，但是java将自动提升变量类型 byte->short->int->float->double
        // 最终找打了提供double的重载方法，然后执行。
        System.out.println("rect test overload=" + rect.getOverload() + ",overload=" + rect.getOverload(5));// 测试重载

        System.out.println("rect test reference=" + rect.equal(squre));// 测试传递引用

        int a = 100;
        rect.callByValue(a);
        System.out.println("call by value=" + a);// 测试传递引用
        rect.callByReference(squre);
        System.out.println("call by reference=" + squre.getW());// 测试传递引用

        Circle circle = new Circle(100);// 创建一个圆形实例
        System.out.println("circle area=" + circle.calcS());// 计算面积

        Circle circle2 = new Circle(50);// 创建一个圆形实例
        System.out.println("circle pi=" + Circle.GetPi());// Pi值不会改变。

        // 数组对象 length属性
        int arra[] = new int[9];
        System.out.println("arra.length=" + arra.length);// 数组实际长度

        squre.recursion(5);
        squre.show();

        System.out.println("测试方法动态调度");
        // 方法动态调度，java根据引用对象类型来执行对应的那个重载方法。
        Rectangle test = null;
        test = rect;
        test.show();// 引用对象类型是Rectange
        test = squre;
        test.show();// 引用对象类型是Square

        circle2.testInner();
    }
}
