import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { X, Send, Mail } from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import { contactAPI } from '../services/api';

const ContactForm = ({ onClose, recipientEmail }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const contactData = {
        ...formData,
        recipient_email: recipientEmail || 'kclynch@uh.edu'
      };

      await contactAPI.submitContact(contactData);
      
      toast({
        title: "Message Sent!",
        description: "Your message has been sent successfully. Kyle will get back to you soon.",
      });
      
      onClose();
    } catch (error) {
      console.error('Contact form error:', error);
      toast({
        title: "Error",
        description: error.response?.data?.detail || "Failed to send message. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-lg bg-gradient-to-br from-yellow-50 via-amber-50 to-orange-100 border-2 border-amber-200 shadow-2xl">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-amber-900 flex items-center gap-2">
              <Mail className="w-6 h-6" />
              Contact Kyle Lynch
            </h2>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="text-amber-600 hover:text-amber-800 hover:bg-amber-100"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <Label htmlFor="name" className="text-amber-800 font-medium">
                  Your Name *
                </Label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                  placeholder="John Doe"
                />
              </div>
              <div>
                <Label htmlFor="email" className="text-amber-800 font-medium">
                  Your Email *
                </Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                  placeholder="john@example.com"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="subject" className="text-amber-800 font-medium">
                Subject *
              </Label>
              <Input
                id="subject"
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                required
                className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                placeholder="Job Opportunity / Project Inquiry"
              />
            </div>

            <div>
              <Label htmlFor="message" className="text-amber-800 font-medium">
                Message *
              </Label>
              <Textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleChange}
                required
                rows={5}
                className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                placeholder="Please describe your opportunity or inquiry..."
              />
            </div>

            <div className="flex gap-3 pt-4">
              <Button
                type="submit"
                disabled={isSubmitting}
                className="flex-1 bg-amber-700 hover:bg-amber-800 text-cream"
              >
                <Send className="w-4 h-4 mr-2" />
                {isSubmitting ? 'Sending...' : 'Send Message'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={onClose}
                className="border-amber-600 text-amber-800 hover:bg-amber-100"
              >
                Cancel
              </Button>
            </div>
          </form>

          <div className="mt-6 pt-4 border-t border-amber-200">
            <p className="text-sm text-amber-600 text-center">
              Direct email: <a href={`mailto:${recipientEmail || 'kclynch@uh.edu'}`} className="hover:text-amber-800 font-medium">{recipientEmail || 'kclynch@uh.edu'}</a>
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default ContactForm;