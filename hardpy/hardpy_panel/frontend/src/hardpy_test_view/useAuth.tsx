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

/**
 * Hook for managing user authentication
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
   * Get session ID for API calls
   */
  const getSessionId = React.useCallback((): string | null => {
    if (!isAuthEnabled) return null;
    return user?.sessionId || null;
  }, [isAuthEnabled, user]);

  /**
   * Validate session with backend
   */
  const validateSessionWithBackend =
    React.useCallback(async (): Promise<boolean> => {
      if (!isAuthEnabled || !user) {
        return true;
      }

      try {
        const response = await fetch("/api/auth/validate_session", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: user.sessionId,
            lastActivity: user.lastActivity,
          }),
        });

        const result = await response.json();
        return result.valid === true;
      } catch (err) {
        console.error("Session validation failed:", err);
        return false;
      }
    }, [isAuthEnabled, user]);

  /**
   * Check if session is expired
   */
  const checkSessionExpiry = React.useCallback(async () => {
    if (!isAuthEnabled || !user) {
      setSessionValid(true);
      return true;
    }

    const isValid = await validateSessionWithBackend();

    if (!isValid) {
      setSessionValid(false);
      setUser(null);
      localStorage.removeItem("hardpy_user");
      return false;
    }

    setSessionValid(true);
    return true;
  }, [isAuthEnabled, user, validateSessionWithBackend]);

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

    // Check every 30 seconds
    sessionCheckRef.current = setInterval(() => {
      checkSessionExpiry();
    }, 30000);

    return () => {
      if (sessionCheckRef.current) {
        clearInterval(sessionCheckRef.current);
      }
    };
  }, [isAuthEnabled, user, checkSessionExpiry]);

  /**
   * Load user from localStorage on component mount and start session validation
   */
  React.useEffect(() => {
    if (!isAuthEnabled) {
      if (user) {
        setUser(null);
        localStorage.removeItem("hardpy_user");
      }
      setSessionValid(true);
      return;
    }

    const savedUser = localStorage.getItem("hardpy_user");
    if (savedUser) {
      try {
        const userData: User = JSON.parse(savedUser);
        setUser(userData);
        setSessionValid(true);

        // Validate session with backend on load
        validateSessionWithBackend().then((isValid) => {
          if (!isValid) {
            setUser(null);
            setSessionValid(false);
            localStorage.removeItem("hardpy_user");
          } else {
            startSessionValidation();
          }
        });
      } catch (e) {
        localStorage.removeItem("hardpy_user");
        setSessionValid(false);
      }
    } else {
      setSessionValid(false);
    }
  }, [isAuthEnabled, startSessionValidation, validateSessionWithBackend]);

  const updateLastActivity = React.useCallback(() => {
    if (user) {
      const updatedUser = { ...user, lastActivity: Date.now() };
      setUser(updatedUser);
      localStorage.setItem("hardpy_user", JSON.stringify(updatedUser));
    }
  }, [user]);

  /**
   * Authenticate user with backend API
   * If authentication is disabled, immediately return true
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
        localStorage.setItem("hardpy_user", JSON.stringify(userData));
        setError(undefined);

        // Start session validation after successful login
        startSessionValidation();

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
    if (user?.sessionId) {
      try {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ session_id: user.sessionId }),
        });
      } catch (err) {
        console.error("Logout request failed:", err);
      }
    }

    setUser(null);
    setSessionValid(false);
    localStorage.removeItem("hardpy_user");

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
