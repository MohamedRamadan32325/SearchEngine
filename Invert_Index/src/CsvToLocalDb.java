import java.io.*;
import java.sql.*;

public class CsvToLocalDb {

    public static void main(String[] args) {
        String csvFile = "inverted_index_sorted.csv";
        String connectionUrl = "jdbc:sqlserver:(localdb)\\MSSQLLocalDB;database=test;integratedSecurity=true;encrypt=true;trustServerCertificate=true";

        String insertSQL = "INSERT INTO InvertedIndex (Word, Filename, Count) VALUES (?, ?, ?)";

        try (
                Connection conn = DriverManager.getConnection(connectionUrl);
                PreparedStatement pstmt = conn.prepareStatement(insertSQL);
                BufferedReader br = new BufferedReader(new FileReader(csvFile));
        ) {
            // Skip header
            String line = br.readLine();

            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",", -1);
                if (parts.length != 3) continue;

                String word = parts[0].trim();
                String filename = parts[1].trim();
                int count = Integer.parseInt(parts[2].trim());

                pstmt.setString(1, word);
                pstmt.setString(2, filename);
                pstmt.setInt(3, count);
                pstmt.addBatch();
            }

            int[] rowsInserted = pstmt.executeBatch();
            System.out.println("Inserted " + rowsInserted.length + " rows into LocalDB.");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
