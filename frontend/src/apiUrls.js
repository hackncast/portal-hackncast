export default {
  'core': [
    {
      'name': 'login',
      'url': '/api/auth/login/',
      'methods': [
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'logout',
      'url': '/api/auth/logout/',
      'methods': [
        'GET',
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'passwordChange',
      'url': '/api/auth/password/change/',
      'methods': [
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'passwordReset',
      'url': '/api/auth/password/reset/',
      'methods': [
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'passwordResetConfirm',
      'url': '/api/auth/password/reset/confirm/',
      'methods': [
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'register',
      'url': '/api/auth/registration/',
      'methods': [
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'userDetails',
      'url': '/api/auth/user/',
      'methods': [
        'GET',
        'PUT',
        'PATCH',
        'OPTIONS'
      ]
    },
    {
      'name': 'verifyEmail',
      'url': '/api/auth/registration/verify-email/',
      'methods': [
        'POST',
        'OPTIONS',
        'HEAD'
      ]
    }
  ],
  'user': [
    {
      'name': 'accessList',
      'url': '/api/user/access/',
      'methods': [
        'GET',
        'OPTIONS'
      ]
    },
    {
      'name': 'blockedOriginFatail',
      'url': '/api/user/access/blocked/{/address}',
      'methods': [
        'DELETE',
        'OPTIONS'
      ]
    },
    {
      'name': 'blockedOriginList',
      'url': '/api/user/access/blocked/',
      'methods': [
        'GET',
        'OPTIONS'
      ]
    },
    {
      'name': 'emailDetail',
      'url': '/api/user/email/{/pk}/',
      'methods': [
        'GET',
        'PUT',
        'DELETE',
        'OPTIONS'
      ]
    },
    {
      'name': 'emailList',
      'url': '/api/user/email/',
      'methods': [
        'GET',
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'passwordChangesList',
      'url': '/api/user/password/',
      'methods': [
        'GET',
        'OPTIONS'
      ]
    },
    {
      'name': 'resendEmailConfirmation',
      'url': '/api/user/email/{/pk}/send_confirmation/',
      'methods': [
        'POST',
        'OPTIONS'
      ]
    },
    {
      'name': 'sessionDetail',
      'url': '/api/user/session/{/pk}/',
      'methods': [
        'GET',
        'DELETE',
        'OPTIONS'
      ]
    },
    {
      'name': 'sessionList',
      'url': '/api/user/session/',
      'methods': [
        'GET',
        'OPTIONS'
      ]
    }
  ]
}
