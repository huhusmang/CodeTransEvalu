// Write the declarations here

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Array;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.LinkedList;
import java.util.Queue;

class Test {
    public static class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    public static ListNode createLinkedList(String s) {
        s = s.replaceAll("[\\[\\]]", "");
        String[] nums = s.split(",");
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        for (String numStr : nums) {
            int num = Integer.parseInt(numStr.trim());
            current.next = new ListNode(num);
            current = current.next;
        }
        return dummy.next;
    }

    public static List<Integer> linkedListToList(ListNode head) {
        List<Integer> list = new ArrayList<>();
        ListNode current = head;
        while (current != null) {
            list.add(current.val);
            current = current.next;
        }
        return list;
    }

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode() {}
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    public static TreeNode createBinaryTree(String data) {
        if(data == ""){
            return null;
        }
        String[] dataList = data.split(",");
        TreeNode root = new TreeNode(Integer.parseInt(dataList[0]));
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int i = 1;
        while (!queue.isEmpty() && i < dataList.length) {
            TreeNode node = queue.poll();
            if (!"null".equals(dataList[i])) {
                node.left = new TreeNode(Integer.parseInt(dataList[i]));
                queue.offer(node.left);
            }
            i++;
            if (i < dataList.length && !"null".equals(dataList[i])) {
                node.right = new TreeNode(Integer.parseInt(dataList[i]));
                queue.offer(node.right);
            }
            i++;
        }
        return root;
    }


    private static String serializeList(List obj) {
        StringBuilder listStr = new StringBuilder("[");
        for (Object item : obj) {
            listStr.append(serializeObj(item));
            listStr.append(",");
        }
        listStr.setCharAt(listStr.length() - 1, ']');
        return listStr.toString();
    }

    private static String serializeArray(Object obj) {
        StringBuilder listStr = new StringBuilder("[");
        for (int i = 0; i < Array.getLength(obj); i++) {
            listStr.append(serializeObj(Array.get(obj, i)));
            listStr.append(",");
        }
        listStr.setCharAt(listStr.length() - 1, ']');
        return listStr.toString();
    }

    private static String serializeDict(Map obj) {
        var m = new TreeMap<Object, Object>();
        for (Object item : obj.entrySet()) {
            m.put(((Map.Entry) item).getKey(), ((Map.Entry) item).getValue());
        }
        StringBuilder mapStr = new StringBuilder("{");
        for (var item : m.entrySet()) {
            mapStr.append(serializeObj(item.getKey()));
            mapStr.append(":");
            mapStr.append(serializeObj(item.getValue()));
            mapStr.append(",");
        }
        mapStr.setCharAt(mapStr.length() - 1, '}');
        return mapStr.toString();
    }

    private static String serializeObj(Object obj) {
        if (obj == null) {
            return "null";
        }
        if (obj instanceof Integer) {
            return String.valueOf(obj);
        }
        if (obj instanceof Long) {
            return String.valueOf(obj);
        }
        if (obj instanceof Double) {
            return String.format("%.6f", obj);
        }
        if (obj instanceof Boolean) {
            return String.valueOf(obj);
        }
        if (obj instanceof Character) {
            return "'" + String.valueOf(obj) + "'";
        }
        if (obj instanceof String) {
            return "\"" + obj + "\"";
        }
        if (obj.getClass().isArray()){
            return serializeArray(obj);
        }
        if (obj instanceof List<?>) {
            return serializeList((List) obj);
        }
        if (obj instanceof Map<?, ?>) {
            return serializeDict((Map) obj);
        }
        if (obj instanceof ListNode) {
            return serializeList(linkedListToList((ListNode) obj));
        }
        throw new RuntimeException("Unrecognized Type!");
    }

    public static Object convertToType(String data, String type) {
        switch (type) {
            case "int":
                return Integer.parseInt(data.trim());
            case "char":
                return data.charAt(0);
            case "String":
                if (data.equals("''") || data.equals("\"\"")) {
                    return "";
                }
                return data;
            case "long":
                return Long.parseLong(data.trim());
            case "boolean":
                return Boolean.parseBoolean(data.trim());
            case "List<List<Integer>>":
                return Arrays.stream(data.trim().split("\\],\\["))
                        .map(s -> s.replaceAll("[\\[\\]]", ""))
                        .map(line -> Arrays.stream(line.split(","))
                                .map(Integer::parseInt)
                                .collect(Collectors.toList()))
                        .collect(Collectors.toList());
            case "List<Integer>":
                return Arrays.stream(data.replaceAll("[\\[\\]\\s]", "").split(","))
                        .map(Integer::parseInt)
                        .collect(Collectors.toList());
            case "int[]":
                return Arrays.stream(data.replaceAll("[\\[\\]\\s]", "").split(","))
                        .mapToInt(Integer::parseInt).toArray();
            case "int[][]":
                return Arrays.stream(data.trim().split("\\],\\["))
                        .map(s -> s.replaceAll("[\\[\\]]", ""))
                        .map(line -> Arrays.stream(line.split(","))
                                .mapToInt(Integer::parseInt).toArray())
                        .toArray(int[][]::new);
            case "List<Long>":
                return Arrays.stream(data.replaceAll("[\\[\\]\\s]", "").split(","))
                        .map(Long::parseLong)
                        .collect(Collectors.toList());
            case "long[]":
                return Arrays.stream(data.replaceAll("[\\[\\]\\s]", "").split(","))
                        .mapToLong(Long::parseLong).toArray();
            case "String[]":
                return data.replaceAll("[\\[\\]'\"\\s]", "").split(",");
            case "List<String>":
                return Arrays.asList(data.replaceAll("[\\[\\]'\"\\s]", "").split(","));
            case "ListNode":
                return createLinkedList(data);
            case "TreeNode":
                return createBinaryTree(data);
            default:
                return null;
        }
    }

    public static boolean areEquivalent(Object o1, Object o2) {
        System.out.println(serializeObj(o1)+" "+serializeObj(o2));
        return serializeObj(o1).equals(serializeObj(o2));
    }

    // Write the target function here
public static long testfunc(int[] nums1, int[] nums2) {
    long s1 = 0;
    boolean zero1 = false;
    for (int x : nums1) {
        if (x == 0) {
            zero1 = true;
            s1++;
        } else {
            s1 += x;
        }
    }
    long s2 = 0;
    boolean zero2 = false;
    for (int x : nums2) {
        if (x == 0) {
            zero2 = true;
            s2++;
        } else {
            s2 += x;
        }
    }
    if (!zero1 && s1 < s2 || !zero2 && s2 < s1) {
        return -1;
    }
    return Math.max(s1, s2);
}
// End here

    public static void start() {
        int total = 0;
        int count = 0;
        // Write the unit tests here

        String[] input_type = {"int[]", "int[]"};
        String output_type = "long";

        int[] data1;
		int[] data2;
        long return_data;
        long gold_ans;

        String basePath = "/home/ubuntu/test_codellm/datas/testcases/2";
        for (int folder = 1; folder <= 5; folder++) {
            String[] inputDatas;
            try (BufferedReader br = new BufferedReader(new FileReader(Paths.get(basePath, folder + "i.txt").toString()))) {
                inputDatas = br.lines().toArray(String[]::new);
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            data1 = (int[])convertToType(inputDatas[0].trim(), input_type[0]);
		data2 = (int[])convertToType(inputDatas[1].trim(), input_type[1]);

            String returnDatas = null;
            try (BufferedReader br = new BufferedReader(new FileReader(Paths.get(basePath, folder + "o.txt").toString()))) {
                returnDatas = br.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }
            gold_ans = (long)convertToType(returnDatas.trim(), output_type);

            return_data = testfunc(data1, data2);

            total += 1;
            if (areEquivalent(return_data, gold_ans)){
                count += 1;
            }
        }
    
// Unit tests end here
        if (count == total) {
            System.out.println("All Passed!");
        } else {
            System.out.println("Failed " + (total - count) + " out of " + total + " tests.");
            System.out.println("Compilation Passed!");
        }
    }

    public static void main(String[] args) {
        start();
    }
}
