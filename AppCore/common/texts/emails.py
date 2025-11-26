EMAIL_CREATE_ACCOUNT = """
<html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Código P/ Nova Conta</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }
            .email-container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                border: 1px solid #e0e0e0;
                max-width: 600px;
                margin: 40px auto;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            .code-container {
                background-color: #4CAF50;
                color: white;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                padding: 15px;
                border-radius: 8px;
                margin: 20px auto;
                max-width: 150px;
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                font-size: 14px;
                color: #666;
            }
            .footer a {
                color: #4CAF50;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <h2>Criação de Conta</h2>
            <p>Olá,</p>
            <p>Recebemos a requisição para criar uma conta com este email. Para validar a criação, use o código abaixo:</p>
            
            <div class="code-container">
            %s
            </div>
            
            <p>Se você não solicitou a criação da conta, por favor, ignore este email.</p>
            
            <div class="footer">
                Sistema de Gestão de Usuários<br>
            </div>
        </div>
    </body>
</html>
"""

EMAIL_PASSWORD_RESET_ACCOUNT = """
<html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Código P/ Redefinição de Senha</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }
            .email-container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                border: 1px solid #e0e0e0;
                max-width: 600px;
                margin: 40px auto;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            .code-container {
                background-color: #4CAF50;
                color: white;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                padding: 15px;
                border-radius: 8px;
                margin: 20px auto;
                max-width: 150px;
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                font-size: 14px;
                color: #666;
            }
            .footer a {
                color: #4CAF50;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <h2>Redefinição de Senha</h2>
            <p>Olá,</p>
            <p>Recebemos a requisição para redefinir a senha da sua conta. Para validar a solicitação, use o código abaixo:</p>

            <div class="code-container">
            %s
            </div>

            <p>Se você não solicitou a redefinição de senha, por favor, ignore este email.</p>
            
            <div class="footer">
                Sistema de Gestão de Usuários<br>
            </div>
        </div>
    </body>
</html>
"""