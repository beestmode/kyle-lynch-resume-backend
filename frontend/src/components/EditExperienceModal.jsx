import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Switch } from './ui/switch';
import { X, Save, Plus, Trash2 } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const EditExperienceModal = ({ experience, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    position: experience.position || '',
    company: experience.company || '',
    location: experience.location || '',
    duration: experience.duration || '',
    description: experience.description || '',
    current: experience.current || false,
    achievements: experience.achievements || []
  });
  const [newAchievement, setNewAchievement] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const updatedExperience = {
        ...experience,
        ...formData
      };
      
      onSave(updatedExperience);
      
      toast({
        title: "Experience Updated!",
        description: "The experience has been successfully updated.",
      });
      
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update experience. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCurrentChange = (checked) => {
    setFormData(prev => ({
      ...prev,
      current: checked
    }));
  };

  const addAchievement = () => {
    if (newAchievement.trim()) {
      setFormData(prev => ({
        ...prev,
        achievements: [...prev.achievements, newAchievement.trim()]
      }));
      setNewAchievement('');
    }
  };

  const removeAchievement = (index) => {
    setFormData(prev => ({
      ...prev,
      achievements: prev.achievements.filter((_, i) => i !== index)
    }));
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <Card className="w-full max-w-2xl bg-gradient-to-br from-yellow-50 via-amber-50 to-orange-100 border-2 border-amber-200 shadow-2xl my-8">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-amber-900">
              Edit Experience
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
                <Label htmlFor="position" className="text-amber-800 font-medium">
                  Position Title *
                </Label>
                <Input
                  id="position"
                  name="position"
                  value={formData.position}
                  onChange={handleChange}
                  required
                  className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                />
              </div>
              <div>
                <Label htmlFor="company" className="text-amber-800 font-medium">
                  Company *
                </Label>
                <Input
                  id="company"
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  required
                  className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                />
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <Label htmlFor="location" className="text-amber-800 font-medium">
                  Location *
                </Label>
                <Input
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  required
                  className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                />
              </div>
              <div>
                <Label htmlFor="duration" className="text-amber-800 font-medium">
                  Duration *
                </Label>
                <Input
                  id="duration"
                  name="duration"
                  value={formData.duration}
                  onChange={handleChange}
                  required
                  placeholder="MM/YY - MM/YY or MM/YY - Present"
                  className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                />
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Switch
                id="current"
                checked={formData.current}
                onCheckedChange={handleCurrentChange}
              />
              <Label htmlFor="current" className="text-amber-800 font-medium">
                This is my current position
              </Label>
            </div>

            <div>
              <Label htmlFor="description" className="text-amber-800 font-medium">
                Job Description *
              </Label>
              <Textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
                rows={4}
                className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                placeholder="Describe your role and responsibilities..."
              />
            </div>

            {/* Achievements Section */}
            <div>
              <Label className="text-amber-800 font-medium">
                Key Achievements (Optional)
              </Label>
              
              {formData.achievements.length > 0 && (
                <div className="space-y-2 mt-2 mb-4">
                  {formData.achievements.map((achievement, index) => (
                    <div key={index} className="flex items-start gap-2 p-3 bg-amber-50 border border-amber-200 rounded">
                      <span className="flex-1 text-sm text-amber-800">{achievement}</span>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeAchievement(index)}
                        className="text-red-600 hover:text-red-800 hover:bg-red-100"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
              
              <div className="flex gap-2">
                <Input
                  value={newAchievement}
                  onChange={(e) => setNewAchievement(e.target.value)}
                  placeholder="Add a key achievement..."
                  className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addAchievement();
                    }
                  }}
                />
                <Button
                  type="button"
                  onClick={addAchievement}
                  variant="outline"
                  className="border-amber-600 text-amber-800 hover:bg-amber-100"
                >
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
            </div>

            <div className="flex gap-3 pt-6 border-t border-amber-200">
              <Button
                type="submit"
                disabled={isSubmitting}
                className="flex-1 bg-amber-700 hover:bg-amber-800 text-cream"
              >
                <Save className="w-4 h-4 mr-2" />
                {isSubmitting ? 'Saving...' : 'Save Changes'}
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
        </div>
      </Card>
    </div>
  );
};

export default EditExperienceModal;