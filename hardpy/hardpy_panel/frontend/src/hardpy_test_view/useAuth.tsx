// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

interface User {
  name: string;
  role: string;
  loginTime: number;
  lastActivity: number;
  sessionId: string;
}

interface AuthConfig {
  enabled?: boolean;
  timeout_minutes?: number;
}

interface FrontendConfig {
  auth?: AuthConfig;
}

interface AppConfig {
  frontend?: FrontendConfig;
}

// Storage keys
const STORAGE_KEYS = {
  USER: "hardpy_user",
  SESSION_ID: "hardpy_session_id",
};

/**
 * Hook for managing user authentication with persistent session storage
 */
export const useAuth = (appConfig: AppConfig | null) => {
  const [user, setUser] = React.useState<User | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | undefined>();
  const [sessionValid, setSessionValid] = React.useState(true);
  const sessionCheckRef = React.useRef<NodeJS.Timeout | null>(null);

  const isAuthEnabled = appConfig?.frontend?.auth?.enabled ?? false;
  const timeoutMinutes = appConfig?.frontend?.auth?.timeout_minutes ?? 60;

  /**
   * Save user data to localStorage
   */
  const saveUserToStorage = React.useCallback((userData: User) => {
    try {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
      localStorage.setItem(STORAGE_KEYS.SESSION_ID, userData.sessionId);
    } catch (e) {
      console.warn("Failed to save user data to localStorage:", e);
    }
  }, []);

  /**
   * Load user data from localStorage
   */
  const loadUserFromStorage = React.useCallback((): User | null => {
    try {
      const userData = localStorage.getItem(STORAGE_KEYS.USER);
      const sessionId = localStorage.getItem(STORAGE_KEYS.SESSION_ID);

      if (userData && sessionId) {
        const parsedUser = JSON.parse(userData);
        // Verify session ID matches
        if (parsedUser.sessionId === sessionId) {
          return parsedUser;
        }
      }
    } catch (e) {
      console.warn("Failed to load user data from localStorage:", e);
    }
    return null;
  }, []);

  /**
   * Clear user data from localStorage
   */
  const clearUserFromStorage = React.useCallback(() => {
    try {
      localStorage.removeItem(STORAGE_KEYS.USER);
      localStorage.removeItem(STORAGE_KEYS.SESSION_ID);
    } catch (e) {
      console.warn("Failed to clear user data from localStorage:", e);
    }
  }, []);

  /**
   * Get session ID for API calls
   */
  const getSessionId = React.useCallback((): string | null => {
    if (!isAuthEnabled) return null;
    return (
      user?.sessionId || localStorage.getItem(STORAGE_KEYS.SESSION_ID) || null
    );
  }, [isAuthEnabled, user]);

  /**
   * Validate session with backend
   */
  const validateSessionWithBackend = React.useCallback(
    async (
      sessionId: string
    ): Promise<{ valid: boolean; user?: { name: string; role: string } }> => {
      if (!isAuthEnabled) {
        return { valid: true };
      }

      try {
        const response = await fetch("/api/auth/validate_session", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            lastActivity: Date.now(),
          }),
        });

        return await response.json();
      } catch (err) {
        console.error("Session validation failed:", err);
        return { valid: false };
      }
    },
    [isAuthEnabled]
  );

  /**
   * Check if session is expired locally
   */
  const isSessionExpiredLocally = React.useCallback(
    (userData: User): boolean => {
      const timeoutMs = timeoutMinutes * 60 * 1000;
      return Date.now() - userData.lastActivity > timeoutMs;
    },
    [timeoutMinutes]
  );

  /**
   * Restore session from storage on component mount
   */
  React.useEffect(() => {
    const restoreSession = async () => {
      if (!isAuthEnabled) {
        setSessionValid(true);
        return;
      }

      const savedUser = loadUserFromStorage();

      if (!savedUser) {
        setSessionValid(false);
        return;
      }

      // Check local expiration first
      if (isSessionExpiredLocally(savedUser)) {
        console.log("Session expired locally");
        clearUserFromStorage();
        setSessionValid(false);
        return;
      }

      // Validate with backend
      const validationResult = await validateSessionWithBackend(
        savedUser.sessionId
      );

      if (validationResult.valid && validationResult.user) {
        // Update user data with backend response
        const updatedUser: User = {
          ...savedUser,
          name: validationResult.user.name,
          role: validationResult.user.role,
          lastActivity: Date.now(),
        };

        setUser(updatedUser);
        saveUserToStorage(updatedUser);
        setSessionValid(true);
        setError(undefined);
      } else {
        console.log("Session validation failed with backend");
        clearUserFromStorage();
        setSessionValid(false);
      }
    };

    restoreSession();
  }, [
    isAuthEnabled,
    loadUserFromStorage,
    clearUserFromStorage,
    validateSessionWithBackend,
    isSessionExpiredLocally,
    saveUserToStorage,
  ]);

  /**
   * Start session validation interval
   */
  const startSessionValidation = React.useCallback(() => {
    if (sessionCheckRef.current) {
      clearInterval(sessionCheckRef.current);
    }

    if (!isAuthEnabled || !user) {
      return;
    }

    // Check every minute
    sessionCheckRef.current = setInterval(async () => {
      if (user) {
        const isValid = await validateSessionWithBackend(user.sessionId);
        if (!isValid.valid) {
          setSessionValid(false);
          setUser(null);
          clearUserFromStorage();
        }
      }
    }, 60000);

    return () => {
      if (sessionCheckRef.current) {
        clearInterval(sessionCheckRef.current);
      }
    };
  }, [isAuthEnabled, user, validateSessionWithBackend, clearUserFromStorage]);

  React.useEffect(() => {
    if (user && isAuthEnabled) {
      startSessionValidation();
    }
  }, [user, isAuthEnabled, startSessionValidation]);

  const updateLastActivity = React.useCallback(() => {
    if (user) {
      const updatedUser = { ...user, lastActivity: Date.now() };
      setUser(updatedUser);
      saveUserToStorage(updatedUser);
    }
  }, [user, saveUserToStorage]);

  /**
   * Authenticate user with backend API
   */
  const login = async (
    username: string,
    password: string
  ): Promise<boolean> => {
    if (!isAuthEnabled) {
      setSessionValid(true);
      return true;
    }

    setIsLoading(true);
    setError(undefined);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const result = await response.json();

      if (result.authenticated) {
        const userData: User = {
          name: result.user.name,
          role: result.user.role,
          loginTime: Date.now(),
          lastActivity: Date.now(),
          sessionId: result.session_id,
        };

        setUser(userData);
        setSessionValid(true);
        saveUserToStorage(userData);
        setError(undefined);

        return true;
      } else {
        setError(result.error || "Authentication failed");
        setSessionValid(false);
        return false;
      }
    } catch (err) {
      setError("Authentication service unavailable. Please try again.");
      setSessionValid(false);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    const sessionId = getSessionId();
    if (sessionId) {
      try {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ session_id: sessionId }),
        });
      } catch (err) {
        console.error("Logout request failed:", err);
      }
    }

    setUser(null);
    setSessionValid(false);
    clearUserFromStorage();

    if (sessionCheckRef.current) {
      clearInterval(sessionCheckRef.current);
    }
  };

  const recordActivity = React.useCallback(() => {
    if (isAuthEnabled && user) {
      updateLastActivity();
    }
  }, [isAuthEnabled, user, updateLastActivity]);

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      if (sessionCheckRef.current) {
        clearInterval(sessionCheckRef.current);
      }
    };
  }, []);

  const isAuthenticated = !isAuthEnabled || (user !== null && sessionValid);

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    recordActivity,
    getSessionId,
    isAuthEnabled,
  };
};
