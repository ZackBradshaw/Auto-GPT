import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final GoogleSignIn googleSignIn = GoogleSignIn(
      clientId:
          "387936576242-iejdacrjljds7hf99q0p6eqna8rju3sb.apps.googleusercontent.com");

// Sign in with Google using redirect
// Sign in with Google using redirect
  Future<UserCredential?> signInWithGoogle() async {
    try {
      final GoogleSignInAccount? googleSignInAccount =
          await googleSignIn.signIn();
      if (googleSignInAccount != null) {
        final GoogleSignInAuthentication googleSignInAuthentication =
            await googleSignInAccount.authentication;
        final AuthCredential credential = GoogleAuthProvider.credential(
          accessToken: googleSignInAuthentication.accessToken,
          idToken: googleSignInAuthentication.idToken,
        );
        return await _auth.signInWithCredential(credential);
      }
    } catch (e) {
      print("Error during Google Sign-In: $e");
      return null;
    }
  }

// Sign in with GitHub using redirect
  Future<UserCredential?> signInWithGitHub() async {
    try {
      final GithubAuthProvider provider = GithubAuthProvider();
      return await _auth.signInWithPopup(provider);
    } catch (e) {
      print("Error during GitHub Sign-In: $e");
      throw e;
    }
  }

  // Sign out
  Future<void> signOut() async {
    await _auth.signOut();
  }

  // Get current user

  // Instructions for configuring GitHub account and generating access token
  /**
   * To configure the GitHub account for authentication, follow these steps:
   * 
   * 1. Go to https://github.com and sign in (or create an account if you don't have one).
   * 2. Navigate to your account settings and then to Developer settings, OAuth Apps.
   * 3. Register a new OAuth application and provide the necessary details.
   * 4. After registering the OAuth application, you will receive a Client ID and Client Secret.
   * 5. Use the Client ID and Client Secret to obtain an access token for authentication in your application.
   * 6. Ensure that the access token is valid and has the required permissions.
   */
  User? getCurrentUser() {
    return _auth.currentUser;
  }
}
