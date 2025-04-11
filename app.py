<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário de Inscrição</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    <style>
        body { background-color: #f1f1f1; font-family: 'Arial', sans-serif; }
        .container { max-width: 800px; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 50px; }
        h2 { text-align: center; color: #f28d35; margin-bottom: 30px; }
        .btn-senac { background-color: #f28d35; color: white; border: none; }
        .btn-senac:hover { background-color: #d9782c; }
        label { font-weight: bold; }
        select, input { margin-bottom: 20px; }
        select, input[type="text"], input[type="number"] { width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
        .form-group { margin-bottom: 25px; }
        .form-control { border-radius: 5px; }
        .logo-container { text-align: center; margin-bottom: 20px; }
        .logo-container img { max-width: 200px; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Logo do SENAC -->
        <div class="logo-container">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo SENAC">
        </div>
        <h2>Formulário de Inscrição</h2>
        <form method="POST" id="formInscricao">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="nome_empresa">Nome da Empresa:</label>
                <input type="text" id="nome_empresa" name="nome_empresa" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="telefone">Telefone para Contato:</label>
                <input type="text" id="telefone" name="telefone" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="cidade">Cidade:</label>
                <select id="cidade" name="cidade" class="form-control" required>
                    <option value="">Selecione uma cidade</option>
                    <option value="Rio Branco">Rio Branco</option>
                    <option value="Cruzeiro do Sul">Cruzeiro do Sul</option>
                </select>
            </div>
            <div class="form-group">
                <label for="segmento">Segmento:</label>
                <select id="segmento" name="segmento" class="form-control" required>
                    <option value="">Selecione um segmento</option>
                </select>
            </div>
            <div class="form-group">
                <label for="curso">Cursos Disponíveis:</label>
                <select id="curso" name="curso" class="form-control" required>
                    <option value="">Selecione um curso</option>
                </select>
            </div>
            <div class="form-group" id="quantidade_alunos_group" style="display:none;">
                <label for="quantidade_alunos">Quantidade de Alunos:</label>
                <input type="number" id="quantidade_alunos" name="quantidade_alunos" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="turno">Turno:</label>
                <select id="turno" name="turno" class="form-control" required>
                    <option value="">Selecione o turno</option>
                    <option value="Manhã">Manhã</option>
                    <option value="Tarde">Tarde</option>
                    <option value="Noite">Noite</option>
                </select>
            </div>
            <div class="form-group text-center">
                <button type="submit" class="btn btn-senac btn-lg w-100">Enviar</button>
            </div>
        </form>
    </div>
  
    <script>
        // Armazenar dados no localStorage ao enviar o formulário
        document.getElementById('formInscricao').addEventListener('submit', function() {
            localStorage.setItem('nome', document.getElementById('nome').value);
            localStorage.setItem('nome_empresa', document.getElementById('nome_empresa').value);
            localStorage.setItem('telefone', document.getElementById('telefone').value);
        });
        // Função para obter parâmetros da URL
        function getQueryParams() {
            var params = {};
            var search = window.location.search.substring(1);
            if (search) {
                search.split('&').forEach(function(part) {
                    var item = part.split('=');
                    params[decodeURIComponent(item[0])] = decodeURIComponent(item[1]);
                });
            }
            return params;
        }
        // Preencher formulário com dados da URL ou localStorage
        window.onload = function() {
            var query = getQueryParams();
            if (query.nome) {
                document.getElementById('nome').value = query.nome;
            } else if (localStorage.getItem('nome')) {
                document.getElementById('nome').value = localStorage.getItem('nome');
            }
            if (query.nome_empresa) {
                document.getElementById('nome_empresa').value = query.nome_empresa;
            } else if (localStorage.getItem('nome_empresa')) {
                document.getElementById('nome_empresa').value = localStorage.getItem('nome_empresa');
            }
            if (query.telefone) {
                document.getElementById('telefone').value = query.telefone;
            } else if (localStorage.getItem('telefone')) {
                document.getElementById('telefone').value = localStorage.getItem('telefone');
            }
        };
        const dadosCidades = {
            "Rio Branco": {
                "Hospedagem": ["Serviços de Camareira", "Técnicas de Recepção em Meios de Hospedagem"],
                "Gastronomia": ["Técnicas para Garçom", "Cozinha Regional", "Preparo de hambúrguer gourmet", "Preparo de Salgados", "Preparo de Saladas"],
                "Turismo": ["Qualidade no Atendimento Turístico"],
                "Saúde": ["Atendente de Farmácia", "Auxiliar em Saúde Bucal", "Coleta de sangue em hemoterapia: doador e paciente", "Cuidador de Idoso", "Cuidador Infantil", "Enfermagem em Hemodiálise e Diálise Peritoneal", "Recepcionista em Serviços de Saúde"],
                "Beleza": ["Cabeleireiro", "Corte Masculino e Feminino", "Depilador", "Manicure e Pedicure", "Técnicas de Maquiagem", "Design de Sobrancelhas", "Modelagem e Henna para Sobrancelhas", "Cortes Masculinos e Design de Barba", "Penteados"],
                "Moda": ["Costureiro", "Modelista"],
                "Produção de alimentos": ["Preparo de Bolos e Tortas", "Preparo de Pizzas", "Técnicas de Confeitaria"],
                "Tecnologia da Informação": ["Assistente de Tecnologias da Informação", "Lei Geral de Proteção de Dados Pessoais (Lgpd)", "Inteligência Artificial na Educação: Melhores Práticas", "Introdução à IA: Inteligência Artificial na Prática", "Segurança de Redes", "Operar Sistemas Operacionais Cliente, Aplicativos de Escritório e Periféricos"],
                "Gestão": ["Licitações e Contratos", "Assistente de Marketing e Vendas", "Assistente Financeiro", "Custos e Formação de Preços", "Recepcionista"],
                "Comércio": ["Ferramentas de Marketing Digital", "Repositor de Mercadorias"],
                "Design": ["Criação de Identidade Visual e Manual de Marca", "Bim - Revit Essencial", "Web Designer"]
            },
            "Cruzeiro do Sul": {
                "Beleza": ["Cabeleireiro", "Manicure e Pedicure", "Barbeiro", "Corte Feminino e Escova", "Técnicas de Unhas Artísticas", "Penteados e Maquiagem para Festas"],
                "Comércio": ["Vendedor", "Operador de Caixa", "Repositor de Mercadorias", "Ferramentas de Marketing Digital", "Formação de Preço"],
                "Gastronomia": ["Técnicas para Garçom", "Preparo de Salgados", "Preparo de hambúrguer gourmet", "Preparo de Saladas"],
                "Gestão": ["Assistente Administrativo", "Assistente de Pessoal", "Assistente de Recursos Humanos", "Excelência no Atendimento ao Cliente", "Recepcionista", "Rotinas de Departamento Pessoal"],
                "Hospedagem": ["Serviços de Camareira", "Técnicas de Recepção em Meios de Hospedagem"],
                "Moda": ["Costureiro"],
                "Produção de alimentos": ["Preparo de Bolos e Tortas", "Técnicas de Confeitaria", "Preparo de Pizzas"],
                "Saúde": ["Enfermagem em Hemodiálise e Diálise Peritoneal", "Atendente de Farmácia", "Cuidador de Idoso", "Agente Comunitário de Saúde", "Coleta de sangue em hemoterapia: doador e paciente", "Assistência de enfermagem materno-infantil", "Qualidade no atendimento em serviços de saúde", "Auxiliar em Saúde Bucal", "Massagista"],
                "Tecnologia da Informação": ["Operar Sistemas Operacionais Cliente, Aplicativos de Escritório e Periféricos", "Assistente de Tecnologias da Informação", "Instalador e Reparador de Redes de Computadores", "Inteligência Artificial na Educação: Melhores Práticas", "Introdução à IA: Inteligência Artificial na Prática", "Segurança de Redes"],
                "Transporte e Armazenagem": ["Frentista"]
            }
        };
        $('#cidade').change(function() {
            const cidadeSelecionada = $(this).val();
            const segmentos = dadosCidades[cidadeSelecionada];
            $('#segmento').empty().append('<option value="">Selecione um segmento</option>');
            for (const segmento in segmentos) {
                $('#segmento').append('<option value="' + segmento + '">' + segmento + '</option>');
            }
        });
        $('#segmento').change(function() {
            const cidadeSelecionada = $('#cidade').val();
            const segmentoSelecionado = $(this).val();
            const cursos = dadosCidades[cidadeSelecionada][segmentoSelecionado];
            $('#curso').empty().append('<option value="">Selecione um curso</option>');
            cursos.forEach(function(curso) {
                $('#curso').append('<option value="' + curso + '">' + curso + '</option>');
            });
        });
        $('#curso').change(function() {
            if ($(this).val() !== '') {
                $('#quantidade_alunos_group').show();
            } else {
                $('#quantidade_alunos_group').hide();
            }
        });
    </script>
</body>
</html>
