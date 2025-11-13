// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

interface User {
  name: string;
  role: string;
  loginTime: number;
  lastActivity: number;
}

/**
 * Hook for managing user authentication
 */
export const useAuth = (
  appConfig: {
    frontend?: { auth_enabled?: boolean; auth_timeout_minutes?: number };
  } | null
) => {
  const [user, setUser] = React.useState<User | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | undefined>();
  const [sessionValid, setSessionValid] = React.useState(true);
  const sessionCheckRef = React.useRef<NodeJS.Timeout | null>(null);

  const isAuthEnabled = appConfig?.frontend?.auth_enabled ?? false;
  const timeoutMinutes = appConfig?.frontend?.auth_timeout_minutes ?? 60;

  /**
   * Check if session is expired
   */
  const checkSessionExpiry = React.useCallback(() => {
    if (!isAuthEnabled || !user) {
      setSessionValid(true);
      return true;
    }

    const minutesInMs = timeoutMinutes * 60 * 1000;
    const isExpired = Date.now() - user.lastActivity > minutesInMs;

    if (isExpired) {
      setSessionValid(false);
      setUser(null);
      localStorage.removeItem("hardpy_user");
      return false;
    }

    setSessionValid(true);
    return true;
  }, [isAuthEnabled, user, timeoutMinutes]);

  /**
   * Start session validation interval
   */
  const startSessionValidation = React.useCallback(() => {
    if (sessionCheckRef.current) {
      clearInterval(sessionCheckRef.current);
    }

    // Check every 10 seconds
    sessionCheckRef.current = setInterval(() => {
      checkSessionExpiry();
    }, 10000);

    return () => {
      if (sessionCheckRef.current) {
        clearInterval(sessionCheckRef.current);
      }
    };
  }, [checkSessionExpiry]);

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
        const minutesInMs = timeoutMinutes * 60 * 1000;
        const isExpired = Date.now() - userData.lastActivity > minutesInMs;

        if (!isExpired) {
          setUser(userData);
          setSessionValid(true);
          startSessionValidation();
        } else {
          localStorage.removeItem("hardpy_user");
          setSessionValid(false);
        }
      } catch (e) {
        localStorage.removeItem("hardpy_user");
        setSessionValid(false);
      }
    } else {
      setSessionValid(false);
    }
  }, [isAuthEnabled, timeoutMinutes, startSessionValidation]);

  const updateLastActivity = React.useCallback(() => {
    if (user) {
      const updatedUser = { ...user, lastActivity: Date.now() };
      setUser(updatedUser);
      localStorage.setItem("hardpy_user", JSON.stringify(updatedUser));

      // Restart session validation to ensure fresh interval
      startSessionValidation();
    }
  }, [user, startSessionValidation]);

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
    isAuthEnabled,
  };
};
