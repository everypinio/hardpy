// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

interface User {
  name: string;
  loginTime: number;
  lastActivity: number;
}

/**
 * Temporary mock authentication
 * Replace with real API calls when backend is ready
 */
const mockAuth = {
  login: async (username: string, password: string): Promise<boolean> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Default credentials for testing
    const validCredentials = [
      { username: "operator", password: "password123" },
      { username: "admin", password: "admin" },
      { username: "test", password: "test" },
    ];

    const isValid = validCredentials.some(
      (cred) => cred.username === username && cred.password === password
    );

    return isValid;
  },

  logout: async (): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
  },
};

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
      return;
    }

    const savedUser = localStorage.getItem("hardpy_user");
    if (savedUser) {
      try {
        const userData: User = JSON.parse(savedUser);
        if (isSessionValid(userData, timeoutHours)) {
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

  const isSessionValid = (userData: User, hours: number): boolean => {
    const now = Date.now();
    const hoursInMs = hours * 60 * 60 * 1000;
    return now - userData.lastActivity < hoursInMs;
  };

  const updateLastActivity = () => {
    if (user) {
      const updatedUser = { ...user, lastActivity: Date.now() };
      setUser(updatedUser);
      localStorage.setItem("hardpy_user", JSON.stringify(updatedUser));
    }
  };

  const login = async (username: string, password: string) => {
    if (!isAuthEnabled) {
      return true;
    }

    setIsLoading(true);
    setError(undefined);

    try {
      // Use mock auth for now - replace with real API call later
      const isAuthenticated = await mockAuth.login(username, password);

      if (isAuthenticated) {
        const userData: User = {
          name: username,
          loginTime: Date.now(),
          lastActivity: Date.now(),
        };

        setUser(userData);
        localStorage.setItem("hardpy_user", JSON.stringify(userData));
        setError(undefined);
        return true;
      } else {
        setError("Invalid username or password");
        return false;
      }
    } catch (err) {
      setError("Authentication error. Please try again.");
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await mockAuth.logout();
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      setUser(null);
      localStorage.removeItem("hardpy_user");
    }
  };

  const isAuthenticated =
    !isAuthEnabled || (user !== null && isSessionValid(user, timeoutHours));

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
