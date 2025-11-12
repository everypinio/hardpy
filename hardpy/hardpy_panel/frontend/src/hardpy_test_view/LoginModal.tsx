// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useTranslation } from "react-i18next";
import {
  Button,
  FormGroup,
  InputGroup,
  Card,
  H2,
  Intent,
} from "@blueprintjs/core";

interface LoginModalProps {
  isVisible: boolean;
  isLoading: boolean;
  error?: string;
  onLogin: (username: string, password: string) => void;
}

/**
 * Modal window for user authentication
 * Blocks the interface until successful login
 */
const LoginModal: React.FC<LoginModalProps> = ({
  isVisible,
  isLoading,
  error,
  onLogin,
}) => {
  const { t } = useTranslation();
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [showPassword, setShowPassword] = React.useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (username.trim() && password.trim()) {
      onLogin(username, password);
    }
  };

  const resetForm = () => {
    setUsername("");
    setPassword("");
    setShowPassword(false);
  };

  React.useEffect(() => {
    if (isVisible) {
      resetForm();
    }
  }, [isVisible]);

  if (!isVisible) {
    return null;
  }

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(255, 255, 255, 0.95)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <Card
        elevation={2}
        style={{
          width: "400px",
          maxWidth: "90vw",
          padding: "20px",
        }}
      >
        <H2 style={{ textAlign: "center", marginBottom: "20px" }}>
          {t("auth.title")}
        </H2>

        <form onSubmit={handleSubmit}>
          <FormGroup
            label={t("auth.username")}
            labelFor="username-input"
            labelInfo="(required)"
          >
            <InputGroup
              id="username-input"
              placeholder={t("auth.usernamePlaceholder")}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
              leftIcon="user"
              large
              intent={error ? Intent.DANGER : Intent.NONE}
            />
          </FormGroup>

          <FormGroup
            label={t("auth.password")}
            labelFor="password-input"
            labelInfo="(required)"
          >
            <InputGroup
              id="password-input"
              placeholder={t("auth.passwordPlaceholder")}
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              leftIcon="lock"
              rightElement={
                <Button
                  icon={showPassword ? "eye-off" : "eye-open"}
                  minimal={true}
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                />
              }
              large
              intent={error ? Intent.DANGER : Intent.NONE}
            />
          </FormGroup>

          {error && (
            <div
              style={{
                color: "#C23030",
                textAlign: "center",
                marginBottom: "15px",
                fontSize: "14px",
              }}
            >
              {error}
            </div>
          )}

          <Button
            type="submit"
            intent={Intent.PRIMARY}
            loading={isLoading}
            disabled={!username.trim() || !password.trim()}
            large
            fill
          >
            {t("auth.loginButton")}
          </Button>
        </form>
      </Card>
    </div>
  );
};

export default LoginModal;
