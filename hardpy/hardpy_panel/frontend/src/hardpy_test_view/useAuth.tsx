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
    frontend?: { auth_enabled?: boolean; auth_timeout_hours?: number };
  } | null
) => {
  const [user, setUser] = React.useState<User | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | undefined>();

  const isAuthEnabled = appConfig?.frontend?.auth_enabled ?? false;
  const timeoutHours = appConfig?.frontend?.auth_timeout_hours ?? 1;

  /**
   * Load user from localStorage on component mount
   */
  React.useEffect(() => {
    if (!isAuthEnabled) {
      if (!user) {
        const defaultUser: User = {
          name: "operator",
          role: "operator",
          loginTime: Date.now(),
          lastActivity: Date.now(),
        };
        setUser(defaultUser);
      }
      return;
    }

    const savedUser = localStorage.getItem("hardpy_user");
    if (savedUser) {
      try {
        const userData: User = JSON.parse(savedUser);
        const hoursInMs = timeoutHours * 60 * 60 * 1000;
        const isExpired = Date.now() - userData.lastActivity > hoursInMs;

        if (!isExpired) {
          setUser(userData);
          updateLastActivity();
        } else {
          localStorage.removeItem("hardpy_user");
        }
      } catch (e) {
        localStorage.removeItem("hardpy_user");
      }
    }
  }, [isAuthEnabled, timeoutHours]);

  const updateLastActivity = () => {
    if (user) {
      const updatedUser = { ...user, lastActivity: Date.now() };
      setUser(updatedUser);
      localStorage.setItem("hardpy_user", JSON.stringify(updatedUser));
    }
  };

  /**
   * Authenticate user with backend API
   */
  const login = async (
    username: string,
    password: string
  ): Promise<boolean> => {
    if (!isAuthEnabled) {
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
        localStorage.setItem("hardpy_user", JSON.stringify(userData));
        setError(undefined);
        return true;
      } else {
        setError(result.error || "Authentication failed");
        return false;
      }
    } catch (err) {
      setError("Authentication service unavailable. Please try again.");
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setUser(null);
    localStorage.removeItem("hardpy_user");
  };

  const isAuthenticated = !isAuthEnabled || user !== null;

  const recordActivity = () => {
    if (isAuthEnabled && user) {
      updateLastActivity();
    }
  };

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
