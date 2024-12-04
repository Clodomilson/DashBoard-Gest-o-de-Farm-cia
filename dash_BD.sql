-- Criação do banco de dados
CREATE DATABASE farmacia_publica;
USE farmacia_publica;

-- Tabela de usuários
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(15) NOT NULL
);

-- Tabela de medicamentos
CREATE TABLE medicamentos (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_medicamento VARCHAR(100) NOT NULL,
    estoque INT NOT NULL DEFAULT 0,
    previsao_reposicao DATE
);

-- Tabela de entregas
CREATE TABLE entregas (
    id_entrega INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_medicamento INT NOT NULL,
    status ENUM('entregue', 'pendente') NOT NULL,
    data_entrega DATE,
    local_entrega VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) ON DELETE CASCADE
);

-- Inserção de dados para teste
INSERT INTO usuarios (nome, email, telefone) VALUES
('Maria Silva', 'maria.silva@email.com', '11987654321'),
('João Santos', 'joao.santos@email.com', '11976543210'),
('Ana Oliveira', 'ana.oliveira@email.com', '11965432109'),
('Ana Souza', 'anasouza@email.com', '(11) 91234-5678'),
('Carlos Lima', 'carloslima@email.com', '(21) 98765-4321'),
('Maria Pereira', 'mariapereira@email.com', '(31) 93456-7890'),
('João Silva', 'joaosilva@email.com', '(41) 99876-5432'),
('Fernanda Costa', 'fernandacosta@email.com', '(51) 92345-6789'),
('Rafael Almeida', 'rafaela@email.com', '(61) 97456-7890'),
('Julia Santos', 'juliasantos@email.com', '(71) 90567-8901'),
('Marcos Oliveira', 'marcos.oliveira@email.com', '(81) 91678-9012'),
('Laura Rodrigues', 'laura.rodrigues@email.com', '(91) 98765-4321'),
('Gabriel Mendes', 'gabrielmendes@email.com', '(11) 92345-6789'),
('Beatriz Carvalho', 'beatrizc@email.com', '(21) 91234-5678'),
('Pedro Silva', 'pedrosilva@email.com', '(31) 90123-4567'),
('Camila Almeida', 'camilalmeida@email.com', '(41) 93012-3456'),
('André Pereira', 'andrepereira@email.com', '(51) 90567-8901'),
('Carolina Ribeiro', 'carol.ribeiro@email.com', '(61) 92345-6789'),
('Felipe Barbosa', 'felipeb@email.com', '(71) 93765-4321'),
('Daniela Martins', 'danielam@email.com', '(81) 91876-5432'),
('Luiz Fernando Gomes', 'luizgomes@email.com', '(91) 92654-3210'),
('Renata Souza', 'renatasouza@email.com', '(11) 93567-8901'),
('Vítor Almeida', 'vitor.almeida@email.com', '(21) 98456-7890'),
('Aline Ferreira', 'alineferreira@email.com', '(31) 90987-6543'),
('Gustavo Costa', 'gustavocosta@email.com', '(41) 95432-6789'),
('Tatiane Rocha', 'tatianerocha@email.com', '(51) 93654-3210'),
('Lucas Oliveira', 'lucasoliveira@email.com', '(61) 91765-4321'),
('Simone Barbosa', 'simoneb@email.com', '(71) 96345-6789'),
('Ricardo Santos', 'ricardosantos@email.com', '(81) 94567-8901'),
('Larissa Lima', 'larissalima@email.com', '(91) 92543-2109'),
('Samuel Rocha', 'samuelrocha@email.com', '(11) 92234-5678'),
('Juliana Martins', 'julianam@email.com', '(21) 93876-5432'),
('Thiago Ribeiro', 'thiagoribeiro@email.com', '(31) 90123-4567');

INSERT INTO medicamentos (nome_medicamento, estoque, previsao_reposicao) VALUES
('Paracetamol', 50, NULL),
('Ibuprofeno', 20, '2024-11-25'),
('Amoxicilina', 5, '2024-11-30'),
('Dipirona', 0, '2024-12-05');

INSERT INTO entregas (id_usuario, id_medicamento, status, data_entrega, local_entrega) VALUES
(1, 1, 'entregue', '2024-11-15', 'UBS São Bernado'),
(1, 2, 'pendente', NULL, 'UBS Vila Palmeira'),
(2, 3, 'pendente', NULL, 'HCM'),
(3, 4, 'pendente', NULL, 'Hospital do Servidor');
