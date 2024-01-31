import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class loginApp extends JFrame {

    private JTextField usernameField;
    private JPasswordField passwordField;

    public loginApp() {
        setTitle("Citas de Carros");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Panel principal con fondo morado claro
        JPanel mainPanel = new JPanel();
        mainPanel.setBackground(new Color(204, 204, 255));
        mainPanel.setLayout(new BorderLayout());

        // Etiqueta de título
        JLabel titleLabel = new JLabel("Citas de Carros");
        titleLabel.setHorizontalAlignment(JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        mainPanel.add(titleLabel, BorderLayout.NORTH);

        // Panel de inicio de sesión
        JPanel loginPanel = new JPanel();
        loginPanel.setLayout(new GridLayout(3, 2));

        JLabel usernameLabel = new JLabel("Usuario:");
        JLabel passwordLabel = new JLabel("Contraseña:");

        usernameField = new JTextField();
        passwordField = new JPasswordField();

        loginPanel.add(usernameLabel);
        loginPanel.add(usernameField);
        loginPanel.add(passwordLabel);
        loginPanel.add(passwordField);

        JButton loginButton = new JButton("Iniciar Sesión");
        loginButton.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                loginButton.setBackground(Color.RED);
            }

            public void mouseExited(java.awt.event.MouseEvent evt) {
                loginButton.setBackground(UIManager.getColor("control"));
            }
        });

        loginButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String username = usernameField.getText();
                String password = new String(passwordField.getPassword());

                if (validateLogin(username, password)) {
                    // Inicio de sesión exitoso, abrir la ventana del negocio
                    openBusinessWindow();
                } else {
                    JOptionPane.showMessageDialog(loginApp.this, "Usuario o contraseña incorrectos", "Error de inicio de sesión", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        loginPanel.add(loginButton);
        mainPanel.add(loginPanel, BorderLayout.CENTER);

        setContentPane(mainPanel);
        setLocationRelativeTo(null);
        setVisible(true);
    }

    private boolean validateLogin(String username, String password) {
        try {
            // Cargar el controlador JDBC de SQLite
            Class.forName("org.sqlite.JDBC");

            // Intenta obtener la conexión
            Connection connection = DriverManager.getConnection("jdbc:sqlite:database.db");
            
            // Imprime un mensaje de éxito si la conexión fue exitosa
            System.out.println("Conexión a la base de datos establecida correctamente.");
    
            String query = "SELECT * FROM usuarios WHERE username=? AND password=?";
            try (PreparedStatement statement = connection.prepareStatement(query)) {
                statement.setString(1, username);
                statement.setString(2, password);
                ResultSet resultSet = statement.executeQuery();
                return resultSet.next();
            }
        } catch (ClassNotFoundException | SQLException e) {
            // Imprime un mensaje de error si hay algún problema
            System.err.println("Error al conectar a la base de datos:");
            e.printStackTrace();
            return false;
        }
    }

    private void openBusinessWindow() {
        // Aquí deberías abrir la ventana del negocio
        // Por ahora, solo mostramos un mensaje
        JOptionPane.showMessageDialog(this, "Bienvenido a la interfaz del negocio", "Inicio de sesión exitoso", JOptionPane.INFORMATION_MESSAGE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new loginApp());
    }
}
