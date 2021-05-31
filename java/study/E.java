package study;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class E {

    public static void quickSort(int[] arra, int start, int end) {
        if (start >= end)
            return;

        int l = start;
        int r = end;
        int value = arra[l];

        while (l < r) {
            while (arra[r] >= value && l < r)
                r--;
            arra[l] = arra[r];
            while (arra[l] <= value && l < r)
                l++;
            arra[r] = arra[l];
        }
        arra[l] = value;
        quickSort(arra, start, l - 1);
        quickSort(arra, l + 1, end);
    }

    public static <Et> void testFan(Et a) {
        System.out.println("is instanceof List=" + (a instanceof List));
        System.out.println("泛型 a=" + a + ",class=" + (a.getClass()));
    }

    public static <Et extends List<Integer>> void testListInterger(Et list) {
        list.add(5);
        System.out.println("list new=" + list);
    }

    public static <Et extends List<?>> void testList(Et list) {
        System.out.println("list.isEmpty()=" + list.isEmpty());
    }

    public static void main(String[] args) {
        // 类集，相当于c语言的stl
        List<Integer> l = new ArrayList<>();// 类似 c++里面的std::vector 数组形式，内存连续，但是有删除操作会有整排位置移动
        l.add(1);
        l.add(1);
        System.out.println("list=" + l.toString());

        List<Long> l2 = new LinkedList<>();// 类似 c++里面的std::list 内存不连续，以链表的形式窜起来有头尾引用。
        l2.add(1L);
        l2.add(1L);
        System.out.println("list2=" + l2.toString());

        Set<Integer> s = new HashSet<>();// 类似 c++的std::set hash散列表结构
        s.add(2);
        s.add(2);
        System.out.println("set=" + s.toString());

        Set<Integer> s2 = new TreeSet<>();// 类似 c++的std::set 树结构
        s2.add(2);
        s2.add(2);
        System.out.println("set2=" + s2.toString());

        Iterator<Integer> it = s2.iterator();
        while (it.hasNext()) {
            System.out.println("next=" + it.next());
        }

        // 不保证键值顺序
        Map<Integer, String> m = new HashMap<>();// 类似 c++的std::map
        m.put(1, "Hello");
        m.put(2, "World");
        System.out.println("map=" + m.toString());

        // 键值按顺序 升序
        Map<Integer, String> m2 = new TreeMap<>();// 类似 c++的std::map
        m2.put(1, "Hello");
        m2.put(2, "World");
        System.out.println("map=" + m2.toString());

        // 展示时间
        Date d = new Date();
        System.out.println(d);

        System.out.println(Math.random());
        System.out.println(new Random().nextInt());

        // 快速排序
        int[] arra = { 8, 2, 10, 4, 8, 9, 7, 6, 1 };
        quickSort(arra, 0, arra.length - 1);
        for (int i = 0; i < arra.length; i++) {
            System.out.println("arra[" + i + "]=" + arra[i]);
        }

        testFan(l);
        testFan(m);

        testListInterger(l);
        testList(l2);
    }
}
