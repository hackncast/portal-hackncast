export default {
  message: {
    'server-error': 'Um erro ocorreu durante a consulta ao servidor, por favor verifique sua conexão com a internet e tente novamente mais tarde.',
    'email-not-confirmed': 'Desculpe, este email ainda não foi confirmado.',
    'default-error': 'Desculpe, seu formulário contém erros!',
    'form-error-heading': 'Os seguintes erros ocorreram durante o envio do formulário:',
    'passwords-must-differ': 'A nova senha deve ser diferente da anterior',
    'invalid-token': 'O token informado é inválido!',
    'profile-updated': 'Perfil atualizado com sucesso!',
    'no-blocked-origin': 'Yay, parece que ninguém está tentando hacker você! Ou talvez eles sejam bons de mais para serem pegos...',
    'unblock-error': 'Um erro ocorreu a realizar remove o bloqueio da origem especificada.',
    'unblock-success': 'Origem liberada com sucesso!'
  },
  dialog: {
    'unverified-email': {
      title: 'Oops... Você já confirmou seu email?',
      text: 'Para poder usufruir de todas as funcionalidades do nosso site, pedimos que você confirme que é dono do seguinte endereço de email:',
      'spam-alert': 'Por favor, verifique sua caixa de entrada e de SPAM. Se não houver um email de confirmação, clique abaixo...'
    },
    'confirm-step': {
      title: 'Só por precaução...',
      text: 'Você tem certeza que deseja prosseguir?'
    },
    'unblock-address': {
      text: 'Você tem certeza que deseja desbloquear o seguinte endereço?',
      alert: 'Se este acesso não foi feito por você, esta ação pode comprometer sua segurança.'
    },
    'access-attempts': {
      title: 'Tentativas de Acesso Incorretas'
    }
  },
  label: {
    'hours': '{hours} hora | {hours} horas',
    'minutes': '{minutes} minuto | {minutes} minutos',
    'seconds': '{seconds} segundo | {seconds} segundos',
    'and': 'e',
    'os': 'OS',
    'engine': 'Motor',
    'browser': 'Navegador',
    'date-and-time': 'Data & Hora',
    'yes': 'Sim',
    'no': 'Não',
    'home': 'Início',
    'lost-your-password': 'Esqueceu sua Senha?',
    'check-your-email': 'Por favor, verifique seu email!',
    'ui': 'Interface',
    'ui-settings': 'Confirgurações de Interface',
    'dark-theme': 'Tema Escuro',
    'send-me-again': 'Enviar novamente...',
    'check-validation': 'Verificar Validação...',
    'passwords': 'Senhas',
    'access-attempt': 'Tentativas de Acesso',
    'blocked-origins': 'Origens Bloqueadas',
    'sessions': 'Sessões',
    'close': 'Fechar',
    'end-session': 'Finalizar Sessão',
    'ip-address': 'Endereço IP',
    'current-session': 'Esta á a sua sessão atual',
    'last-activity': 'Última atividade',
    'registration': 'Cadastramento',
    'thank-you': 'Obrigado!',
    'email': 'Email',
    'emails': 'Emails',
    'password': 'Senha',
    'new-password': 'Nova Senha',
    'old-password': 'Antiga Senha',
    'confirm-email': 'Confirme seu Email',
    'confirm-password': 'Confirmar Senha',
    'confirm-new-password': 'Confirmar Nova Senha',
    'reset-password': 'Resetar Senha',
    'register': 'Cadastrar-se',
    'already-registered': 'Já é Cadastrado?',
    'avatar-alt': 'Avatar de {email}',
    'next': 'Próximo',
    'remember-me': 'Lembrar de mim',
    'login': 'Login',
    'logout': 'Logout',
    'need-help': 'Precisa de Ajuda?',
    'expires': 'Expira',
    'change-password': 'Alterar Senha',
    'level': 'Nível',
    'experience': 'Experiência',
    'security': 'Segurança',
    'registered-emails': 'Emails Cadastrados',
    'account': 'Conta',
    'verified': 'Validado',
    'not-verified': 'Validação pendente!',
    'resend-verification': 'Reenviar Validação',
    'exclude': 'Excluir',
    'cancel': 'Cancelar',
    'change': 'Alterar',
    'set-as-primary': 'Definir como Principal',
    'new-email': 'Novo Email',
    'add': 'Adicionar',
    'attention': 'Atenção',
    'general': 'Geral',
    'confirm': 'Confirmar!',
    'i-remembered-my-password': 'Lembrei da minha senha!',
    'personal-info': 'Dados Pessoais',
    'joined-at': 'Registrado em {date}',
    'username': 'Nome de Usuário',
    'first-name': 'Primeiro Nome',
    'last-name': 'Sobrenome',
    'save': 'Salvar'
  },
  helper: {
    'dark-ui': 'Utilize o tema escuro em ambientes com pouca iluminação.',
    'ui-language': 'Linguagem utilizada na interface',
    'email-confirmation': 'Por favor, clique no botão abaixo para validar o seu endereço de email.'
  },
  profile: {
    'new-email-address': 'Novo Endereço de Email',
    'change-email-attention': '{attention} O email deve ser verificado antes de ser configurado como endereço principal.',
    'change-primary-email': 'Alterar o Email Principal',
    'last-login': 'Último login em {lastLogin}',
    'primary-email': 'Email principal, {email}',
    session: {
      'no-location': 'Localização Indefinida',
      'approximate-location': 'Local de Acesso Aproximado',
      'no-active-sessions': 'Nenhuma sessão ativa foi encontrada'
    },
    attempts: {
      failed: '{failCount} tentativa incorreta de login | {failCount} tentativas incorretas de login',
      origin: '{ipsCount} origem diferente | {ipsCount} origens diferentes',
      found: 'Nos encontramos {failed} de {origin} nos últimos 7 dias.'
    },
    passwordChange: 'Ei, você ainda utiliza a mesma senha desde {dateJoined}? Por favor, considere troca-la em breve... | Você modificou sua senha apenas uma vez, em {lastChanged}. | Você já modificou sua senha {count} vezes. A última vez foi em {lastChanged}.',
    blockedOrigin: {
      title: 'Origem {address} bloqueada há {ago}.',
      waiting: 'Será desbloqueada em {countdown}',
      unlocked: 'Esta origem foi desbloqueada!'
    }
  }
}
