// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useEffect, useState } from "react";
import { Button, Classes, Dialog } from "@blueprintjs/core";

export function StartStandCloudWindow({
  isOpen,
  onClose,
}: {
  isOpen: boolean;
  onClose: () => void;
}) {
  const [registrationLink, setRegistrationLink] = useState("");
  const [connectionStatus, setConnectionStatus] = useState("");

  const handleRegistration = async () => {
    try {
      const response = await fetch("/api/standcloud/register");
      if (response.ok) {
        const data = await response.json();
        setRegistrationLink(data.auth_address);
        setConnectionStatus("");
      } else {
        setRegistrationLink("Failed to get registration link");
      }
    } catch (error) {
      setRegistrationLink("Error occurred while fetching registration link");
    }
  };

  const handleCheckConnection = async () => {
    try {
      const response = await fetch("/api/standcloud/check_connection");
      if (response.ok) {
        const data = await response.json();
        setConnectionStatus(data.connection_status);
        setRegistrationLink("");
      } else {
        setConnectionStatus("Failed to check connection");
      }
    } catch (error) {
      setConnectionStatus("Error occurred while checking connection");
    }
  };

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [onClose]);

  return (
    <Dialog
      title={
        <div>
          <a
            href="https://everypin.io/standcloud"
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: "underline", color: "inherit" }}
          >
            StandCloud
          </a>
          <br />
        </div>
      }
      icon="cloud"
      isOpen={isOpen}
      onClose={onClose}
      canOutsideClickClose={false}
      style={{
        maxWidth: "60%",
        minWidth: "300px",
        height: "25vh",
        minHeight: "200px",
      }}
    >
      <div
        className={Classes.DIALOG_BODY}
        style={{
          wordWrap: "break-word",
          wordBreak: "break-word",
          overflowY: "auto",
          padding: "10px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Button
          intent="primary"
          onClick={handleRegistration}
          style={{ width: "100%", marginBottom: "10px", textAlign: "center" }}
        >
          Registration
        </Button>
        <Button
          intent="primary"
          onClick={handleCheckConnection}
          style={{ width: "100%", marginBottom: "10px", textAlign: "center" }}
        >
          Check Connection
        </Button>
        {registrationLink && (
          <div style={{ textAlign: "center", marginTop: "10px" }}>
            <a
              href={registrationLink}
              target="_blank"
              rel="noopener noreferrer"
            >
              {registrationLink}
            </a>
          </div>
        )}
        {connectionStatus && (
          <div style={{ textAlign: "center", marginTop: "10px" }}>
            {connectionStatus}
          </div>
        )}
      </div>
    </Dialog>
  );
}

export default StartStandCloudWindow;
