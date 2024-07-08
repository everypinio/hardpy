import React, { useState } from 'react';
import { Classes, Dialog } from '@blueprintjs/core';

interface DialogBoxProps {
    title_bar: string;
    dialog_text: string;
    widget_info?: {
      text: { text: string };
      type: string;
    }
}

export function StartConfirmationDialog(props: DialogBoxProps) {

    const [dialogOpen, setDialogOpen] = useState(true);
  
    return (
      <div style={{ display: 'block', width: 400, padding: 30 }}>
        <h4>ReactJS Blueprint Dialog Component</h4>
        <Dialog
          title="Dialog Title"
          icon="info-sign"
          isOpen={dialogOpen}
          onClose={() => setDialogOpen(false)}
        >
          <div className={Classes.DIALOG_BODY}>
            <p>Sample Dialog Content to display!</p>
          </div>
        </Dialog>
      </div>
    );
  }

export default StartConfirmationDialog