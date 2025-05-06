import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Invert_index {

    static class WordCount {
        String filename;
        int count;

        WordCount(String filename, int count) {
            this.filename = filename;
            this.count = count;
        }
    }

    public static void main(String[] args) throws IOException {
        String dirPath = "../output/content";
        String outputCSV = "../output/inverted_index_sorted.csv";

        Map<String, List<WordCount>> invertedIndex = new TreeMap<>(); // Sorted by word

        File dir = new File(dirPath);
        File[] files = dir.listFiles((d, name) -> name.endsWith(".txt"));

        if (files == null) {
            System.err.println("Directory not found or no .txt files.");
            return;
        }

        for (File file : files) {
            String content = new String(Files.readAllBytes(file.toPath()));
            String[] words = content.split("\\W+");
            Map<String, Integer> wordCounts = new HashMap<>();

            for (String w : words) {
                String word = w.toLowerCase();
                if (word.isEmpty()) continue;
                wordCounts.put(word, wordCounts.getOrDefault(word, 0) + 1);
            }

            for (Map.Entry<String, Integer> entry : wordCounts.entrySet()) {
                String word = entry.getKey();
                int count = entry.getValue();

                invertedIndex
                        .computeIfAbsent(word, k -> new ArrayList<>())
                        .add(new WordCount(file.getName(), count));
            }
        }

        // Sort filenames for each word
        for (List<WordCount> list : invertedIndex.values()) {
            list.sort(Comparator.comparing(wc -> wc.filename));
        }

        // Write to CSV
        try (PrintWriter writer = new PrintWriter(new FileWriter(outputCSV))) {
            writer.println("Word,Filename,Count");
            for (Map.Entry<String, List<WordCount>> entry : invertedIndex.entrySet()) {
                String word = entry.getKey();
                for (WordCount wc : entry.getValue()) {
                    writer.printf("%s,%s,%d%n", word, wc.filename, wc.count);
                }
            }
        }

        System.out.println("Sorted inverted index written to: " + outputCSV);
    }
}
