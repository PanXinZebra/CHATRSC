namespace RenderNew
{
    partial class Form2
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.panel3 = new System.Windows.Forms.Panel();
            this.panel4 = new System.Windows.Forms.Panel();
            this.panel6 = new System.Windows.Forms.Panel();
            this.textBox5 = new System.Windows.Forms.TextBox();
            this.button8 = new System.Windows.Forms.Button();
            this.panel5 = new System.Windows.Forms.Panel();
            this.chromiumWebBrowser1 = new CefSharp.WinForms.ChromiumWebBrowser();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.panel3.SuspendLayout();
            this.panel4.SuspendLayout();
            this.panel6.SuspendLayout();
            this.panel5.SuspendLayout();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.BackColor = System.Drawing.Color.DarkSlateGray;
            this.pictureBox1.Location = new System.Drawing.Point(35, 31);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(870, 794);
            this.pictureBox1.TabIndex = 1;
            this.pictureBox1.TabStop = false;
            // 
            // panel3
            // 
            this.panel3.BackColor = System.Drawing.Color.NavajoWhite;
            this.panel3.Controls.Add(this.pictureBox1);
            this.panel3.Location = new System.Drawing.Point(85, 40);
            this.panel3.Name = "panel3";
            this.panel3.Size = new System.Drawing.Size(1085, 1003);
            this.panel3.TabIndex = 5;
            // 
            // panel4
            // 
            this.panel4.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.panel4.Controls.Add(this.panel6);
            this.panel4.Controls.Add(this.panel5);
            this.panel4.Dock = System.Windows.Forms.DockStyle.Right;
            this.panel4.Location = new System.Drawing.Point(1606, 0);
            this.panel4.Name = "panel4";
            this.panel4.Size = new System.Drawing.Size(410, 1116);
            this.panel4.TabIndex = 6;
            // 
            // panel6
            // 
            this.panel6.Controls.Add(this.textBox5);
            this.panel6.Controls.Add(this.button8);
            this.panel6.Location = new System.Drawing.Point(0, 903);
            this.panel6.Name = "panel6";
            this.panel6.Size = new System.Drawing.Size(410, 100);
            this.panel6.TabIndex = 1;
            // 
            // textBox5
            // 
            this.textBox5.Location = new System.Drawing.Point(6, 16);
            this.textBox5.Multiline = true;
            this.textBox5.Name = "textBox5";
            this.textBox5.Size = new System.Drawing.Size(299, 72);
            this.textBox5.TabIndex = 1;
            // 
            // button8
            // 
            this.button8.Location = new System.Drawing.Point(311, 16);
            this.button8.Name = "button8";
            this.button8.Size = new System.Drawing.Size(96, 72);
            this.button8.TabIndex = 0;
            this.button8.Text = "发送";
            this.button8.UseVisualStyleBackColor = true;
            // 
            // panel5
            // 
            this.panel5.Controls.Add(this.chromiumWebBrowser1);
            this.panel5.Location = new System.Drawing.Point(48, 50);
            this.panel5.Name = "panel5";
            this.panel5.Size = new System.Drawing.Size(410, 1003);
            this.panel5.TabIndex = 0;
            // 
            // chromiumWebBrowser1
            // 
            this.chromiumWebBrowser1.ActivateBrowserOnCreation = false;
            this.chromiumWebBrowser1.Location = new System.Drawing.Point(104, 122);
            this.chromiumWebBrowser1.Name = "chromiumWebBrowser1";
            this.chromiumWebBrowser1.Size = new System.Drawing.Size(252, 806);
            this.chromiumWebBrowser1.TabIndex = 0;
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(2016, 1116);
            this.Controls.Add(this.panel4);
            this.Controls.Add(this.panel3);
            this.Name = "Form2";
            this.Text = "Form2";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.panel3.ResumeLayout(false);
            this.panel4.ResumeLayout(false);
            this.panel6.ResumeLayout(false);
            this.panel6.PerformLayout();
            this.panel5.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Panel panel3;
        private System.Windows.Forms.Panel panel4;
        private System.Windows.Forms.Panel panel6;
        private System.Windows.Forms.TextBox textBox5;
        private System.Windows.Forms.Button button8;
        private System.Windows.Forms.Panel panel5;
        private CefSharp.WinForms.ChromiumWebBrowser chromiumWebBrowser1;
    }
}