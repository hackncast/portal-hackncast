export default {
  message: {
    'server-error': 'An error ocurred while quering the server, please check your internet connection and try again later.',
    'email-not-confirmed': 'Sorry, this email hasn\'t been confirmed.',
    'default-error': 'Sorry, your form still have errors!',
    'form-error-heading': 'The following errors ocurred while submitting your form:',
    'passwords-must-differ': 'The new password must differ from tha last one',
    'invalid-token': 'The informed token is invalid!',
    'profile-updated': 'Profile updated successfully!',
    'no-blocked-origin': 'Yay, seems like no one is trying to hack you! Or maybe they\'re too good to be catched...',
    'unblock-error': 'Um erro ocorreu a realizar remove o bloqueio da origem especificada.',
    'unblock-success': 'Origin successfully unblocked!'
  },
  dialog: {
    'unverified-email': {
      title: 'Oops... Have you confirmed your email?',
      text: 'In order to enjoy all our site features, we request you to confirm the ownership of the following email address:',
      'spam-alert': 'Please, check your inbox and SPAM box. If there is no email, please click below...'
    },
    'confirm-step': {
      title: 'Just for caution...',
      text: 'Are you sure you want to proceed?'
    },
    'unblock-address': {
      text: 'Are you sure you want to unblock the following address?',
      alert: 'If this access attempt wasn\'t made by you, this action can compromise your security.'
    },
    'access-attempts': {
      title: 'Failed Access Attempts'
    }
  },
  label: {
    'hours': '{hours} hour | {hours} hours',
    'minutes': '{minutes} minute | {minutes} minutes',
    'seconds': '{seconds} second | {seconds} seconds',
    'and': 'and',
    'os': 'OS',
    'engine': 'Engine',
    'browser': 'Browser',
    'date-and-time': 'Date & Time',
    'yes': 'Yes',
    'no': 'No',
    'home': 'Home',
    'lost-your-password': 'Lost Your Password?',
    'check-your-email': 'Please, check your email!',
    'ui': 'User Interface',
    'ui-settings': 'User Interface Settings',
    'dark-theme': 'Dark Theme',
    'send-me-again': 'Send-me Again...',
    'check-validation': 'Check Validation...',
    'passwords': 'Passwords',
    'access-attempt': 'Access Attempt',
    'blocked-origins': 'Blocked Origins',
    'sessions': 'Sessions',
    'close': 'Close',
    'end-session': 'End Session',
    'ip-address': 'IP Address',
    'current-session': 'This is your current session.',
    'last-activity': 'Last activity',
    'registration': 'Registration',
    'thank-you': 'Thank you!',
    'email': 'Email',
    'emails': 'Emails',
    'password': 'Password',
    'old-password': 'Old Password',
    'new-password': 'New Password',
    'confirm-email': 'Confirm Your Email',
    'confirm-password': 'Confirm Password',
    'confirm-new-password': 'Confirm New Password',
    'reset-password': 'Reset Password',
    'register': 'Register',
    'already-registered': 'Already registered?',
    'avatar-alt': 'Avatar of {email}',
    'next': 'Next',
    'remember-me': 'Remember me',
    'login': 'Login',
    'logout': 'Logout',
    'need-help': 'Need help?',
    'expires': 'Expires',
    'change-password': 'Change Password',
    'level': 'Level',
    'experience': 'Experience',
    'security': 'Security',
    'registered-emails': 'Registered Emails',
    'account': 'Account',
    'verified': 'Verified',
    'not-verified': 'Not verified yet!',
    'resend-verification': 'Resend Verification',
    'exclude': 'Exclude',
    'cancel': 'Cancel',
    'change': 'Change',
    'set-as-primary': 'Set as Primary',
    'new-email': 'New Email',
    'add': 'Add',
    'attention': 'Attention',
    'general': 'General',
    'confirm': 'Confirm!',
    'i-remembered-my-password': 'I remembered my password!',
    'personal-info': 'Personal Informations',
    'joined-at': 'Joined at {date}',
    'username': 'Username',
    'first-name': 'First Name',
    'last-name': 'Last Name',
    'save': 'Save'
  },
  helper: {
    'dark-ui': 'Use the darke theme in lower ligths environments.',
    'ui-language': 'User Interface Language',
    'email-confirmation': 'Please click in the button bellow to validate your email address.'
  },
  profile: {
    'new-email-address': 'New Email Address',
    'change-primary-email': 'Change Primary Email Address',
    'change-email-attention': '{attention} An email must be verified before being set as primary.',
    'last-login': 'Last login at {lastLogin}',
    'primary-email': 'Primary email, {email}',
    session: {
      'no-location': 'No Location Defined',
      'approximate-location': 'Approximated Access Location',
      'no-active-sessions': 'No active sessions found'
    },
    attempts: {
      failed: '{failCount} failed login attempt | {failCount} failed login attempts',
      origin: '{ipsCount} different origin | {ipsCount} different origins',
      found: 'We\'ve found {failed} from {origin} in the last 7 days.'
    },
    passwordChange: 'Hey, you still use your first password from {dateJoined}? Please, consider changing it soon... | You have changed your password one time, on {lastChanged}. | You have changed your password {count} times. Last time was {lastChanged}.',
    blockedOrigin: {
      title: 'Origin {address} locked out {ago}.',
      waiting: 'Will be unlocked in {countdown}',
      unlocked: 'This origin was unlocked!'
    }
  }
}
