package study;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class I {

    static Lock sMutex;
    static int sCount = 10;

    // synchronized 防止线程相互竞争
    synchronized static void play(String name) {
        System.out.println("当前线程：" + Thread.currentThread() + ",name=" + name);
        while (sCount > 0) {
            System.out.println(name + ",sCount=" + sCount--);
            // try {
            // Thread.sleep(1000);
            // } catch (InterruptedException e) {
            // e.printStackTrace();
            // }
        }
    }

    static void play2(String name) {
        System.out.println("当前线程：" + Thread.currentThread() + ",name=" + name);
        while (sCount > 0) {
            System.out.println(name + ",sCount=" + sCount--);
        }
    }

    public static void main(String[] args) {
        // 多线程
        sMutex = new ReentrantLock();// 可重入锁
        sMutex.lock();// 进入临界区
        // 自己的逻辑。。。
        sMutex.unlock();// 离开临界区

        System.out.println("主线程：" + Thread.currentThread());
        Thread t1 = new Thread(new Runnable() {

            @Override
            public void run() {
                play("线程1");

                // synchronized第二种用法
                // synchronized (实例对象)) {
                // // 互斥逻辑
                // }
            }
        });
        Thread t2 = new Thread(new Runnable() {

            @Override
            public void run() {
                play("线程2");
            }

        });
        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}