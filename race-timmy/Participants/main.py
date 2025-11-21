#!/usr/bin/env python3
"""
Race Timmy - 3D Racing Simulation
Cobra (Reference Implementation)
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import time

from car_controller import CarController


class LidarSensor:
    """Simulates a LIDAR sensor with 90-degree field of view"""
    
    def __init__(self, range_max=50.0):
        self.range_max = range_max
        self.num_rays = 91  # -45 to +45 degrees, inclusive
        self.angles = np.linspace(-45, 45, self.num_rays)
    
    def scan(self, car_pos, car_angle, track):
        """
        Returns list of 91 distances from -45° to +45°
        car_pos: (x, y) position
        car_angle: rotation in degrees
        track: Track object with walls
        """
        distances = []
        
        for angle_offset in self.angles:
            # Calculate ray direction
            ray_angle = math.radians(car_angle + angle_offset)
            ray_dir = np.array([math.cos(ray_angle), math.sin(ray_angle)])
            
            # Cast ray and find intersection with track walls
            distance = self._cast_ray(car_pos, ray_dir, track)
            distances.append(min(distance, self.range_max))
        
        return distances
    
    def _cast_ray(self, origin, direction, track):
        """Cast a ray and return distance to nearest wall"""
        min_distance = self.range_max
        
        for wall in track.walls:
            distance = self._ray_segment_intersection(origin, direction, wall)
            if distance is not None and distance < min_distance:
                min_distance = distance
        
        return min_distance
    
    def _ray_segment_intersection(self, ray_origin, ray_dir, segment):
        """Calculate intersection between ray and line segment"""
        p1, p2 = segment
        v1 = ray_origin - p1
        v2 = p2 - p1
        v3 = np.array([-ray_dir[1], ray_dir[0]])
        
        denom = np.dot(v2, v3)
        if abs(denom) < 1e-6:
            return None
        
        # Use 2D cross product manually to avoid numpy warning
        t1 = (v2[0] * v1[1] - v2[1] * v1[0]) / denom
        t2 = np.dot(v1, v3) / denom
        
        if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
            return t1
        
        return None


class Track:
    """Race track with walls"""
    
    def __init__(self):
        # Define track as a series of wall segments (outer and inner boundaries)
        # Simple oval track
        self.walls = []
        self._create_oval_track()
        
        # Start/finish line (between inner and outer walls at bottom)
        self.start_line = (np.array([-5, -15]), np.array([5, -15]))
        self.lap_triggered = False
    
    def _create_oval_track(self):
        """Create an oval track"""
        # Outer boundary
        outer_points = []
        inner_points = []
        
        num_points = 60
        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * math.pi
            
            # Oval shape (wider than tall)
            x = 30 * math.cos(angle)
            y = 20 * math.sin(angle)
            outer_points.append(np.array([x, y]))
            
            # Inner boundary (smaller oval)
            x_inner = 20 * math.cos(angle)
            y_inner = 12 * math.sin(angle)
            inner_points.append(np.array([x_inner, y_inner]))
        
        # Create wall segments
        for i in range(len(outer_points) - 1):
            self.walls.append((outer_points[i], outer_points[i + 1]))
            self.walls.append((inner_points[i], inner_points[i + 1]))
    
    def check_collision(self, pos, radius=1.0):
        """Check if position collides with track walls"""
        for wall in self.walls:
            if self._point_to_segment_distance(pos, wall) < radius:
                return True
        return False
    
    def _point_to_segment_distance(self, point, segment):
        """Calculate distance from point to line segment"""
        p1, p2 = segment
        line_vec = p2 - p1
        point_vec = point - p1
        line_len = np.linalg.norm(line_vec)
        
        if line_len < 1e-6:
            return np.linalg.norm(point_vec)
        
        line_unitvec = line_vec / line_len
        proj_length = np.dot(point_vec, line_unitvec)
        proj_length = max(0, min(line_len, proj_length))
        
        nearest = p1 + line_unitvec * proj_length
        return np.linalg.norm(point - nearest)
    
    def check_lap_completion(self, old_pos, new_pos):
        """Check if car crossed start/finish line"""
        # Simple line crossing detection
        p1, p2 = self.start_line
        
        # Check if trajectory crosses the line
        if self._segments_intersect(old_pos, new_pos, p1, p2):
            return True
        return False
    
    def _segments_intersect(self, a1, a2, b1, b2):
        """Check if two line segments intersect"""
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        return ccw(a1, b1, b2) != ccw(a2, b1, b2) and ccw(a1, a2, b1) != ccw(a1, a2, b2)
    
    def render(self):
        """Render track in 3D"""
        # Draw track surface (darker gray)
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        for i in range(0, len(self.walls) // 2 - 1):
            # Get outer and inner wall segments
            outer1, outer2 = self.walls[i * 2]
            inner1, inner2 = self.walls[i * 2 + 1]
            
            # Draw track surface quad
            glVertex3f(outer1[0], 0.05, outer1[1])
            glVertex3f(outer2[0], 0.05, outer2[1])
            glVertex3f(inner2[0], 0.05, inner2[1])
            glVertex3f(inner1[0], 0.05, inner1[1])
        glEnd()
        
        # Draw solid walls
        glColor3f(0.5, 0.5, 0.5)
        for wall in self.walls:
            p1, p2 = wall
            # Draw solid wall faces
            glBegin(GL_QUADS)
            # Front face
            glVertex3f(p1[0], 0, p1[1])
            glVertex3f(p2[0], 0, p2[1])
            glVertex3f(p2[0], 2, p2[1])
            glVertex3f(p1[0], 2, p1[1])
            glEnd()
        
        # Draw wall outlines for definition
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINES)
        for wall in self.walls:
            p1, p2 = wall
            # Bottom edge
            glVertex3f(p1[0], 0, p1[1])
            glVertex3f(p2[0], 0, p2[1])
            # Top edge
            glVertex3f(p1[0], 2, p1[1])
            glVertex3f(p2[0], 2, p2[1])
            # Vertical edges
            glVertex3f(p1[0], 0, p1[1])
            glVertex3f(p1[0], 2, p1[1])
            glVertex3f(p2[0], 0, p2[1])
            glVertex3f(p2[0], 2, p2[1])
        glEnd()
        
        # Draw start/finish line
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(5)
        glBegin(GL_LINES)
        p1, p2 = self.start_line
        glVertex3f(p1[0], 0.1, p1[1])
        glVertex3f(p2[0], 0.1, p2[1])
        glEnd()
        glLineWidth(1)


class Car:
    """Car with physics simulation"""
    
    def __init__(self, x=0, y=-17.0):  # Start further back, outside the track
        self.pos = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.angle = 0.0  # degrees, 0 is right (into the track), 90 is up
        self.wheel_angle = 0.0  # steering angle
        
        self.acceleration = 0.0
        self.max_speed = 30.0
        self.friction = 0.95
        self.turn_speed = 3.0
        
        self.size = 1.5
        self.crashed = False
        
        print(f"Car initialized at position: {self.pos}, angle: {self.angle}")
    
    def update(self, dt, track):
        """Update car physics"""
        # Apply acceleration
        angle_rad = math.radians(self.angle)
        accel_vec = np.array([
            math.cos(angle_rad) * self.acceleration,
            math.sin(angle_rad) * self.acceleration
        ])
        
        self.velocity += accel_vec * dt
        
        # Apply friction
        self.velocity *= self.friction
        
        # Limit speed
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed
        
        # Apply steering (only when moving)
        if speed > 0.5:
            turn_amount = self.wheel_angle * self.turn_speed * dt * (speed / self.max_speed)
            self.angle += turn_amount
        
        # Update position
        old_pos = self.pos.copy()
        self.pos += self.velocity * dt
        
        # Check collision - just bounce back, don't stop
        if track.check_collision(self.pos, self.size):
            self.pos = old_pos
            self.velocity *= -0.3  # Bounce back with reduced speed
            self.crashed = True
            print(f"Hit wall at position {self.pos}")
        else:
            self.crashed = False  # Reset crash state when clear
        
        return old_pos
    
    def render(self):
        """Render car in 3D"""
        glPushMatrix()
        glTranslatef(self.pos[0], 1.0, self.pos[1])
        glRotatef(-self.angle + 90, 0, 1, 0)
        
        # Car body - much bigger and more visible
        if self.crashed:
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(1.0, 0.3, 0.0)  # Bright orange
        
        # Main body
        glBegin(GL_QUADS)
        # Top
        glVertex3f(-1.5, 1.5, -2.5)
        glVertex3f(1.5, 1.5, -2.5)
        glVertex3f(1.5, 1.5, 2.5)
        glVertex3f(-1.5, 1.5, 2.5)
        # Front
        glVertex3f(-1.5, 0, 2.5)
        glVertex3f(1.5, 0, 2.5)
        glVertex3f(1.5, 1.5, 2.5)
        glVertex3f(-1.5, 1.5, 2.5)
        # Back
        glVertex3f(-1.5, 0, -2.5)
        glVertex3f(1.5, 0, -2.5)
        glVertex3f(1.5, 1.5, -2.5)
        glVertex3f(-1.5, 1.5, -2.5)
        # Left side
        glVertex3f(-1.5, 0, -2.5)
        glVertex3f(-1.5, 1.5, -2.5)
        glVertex3f(-1.5, 1.5, 2.5)
        glVertex3f(-1.5, 0, 2.5)
        # Right side
        glVertex3f(1.5, 0, -2.5)
        glVertex3f(1.5, 1.5, -2.5)
        glVertex3f(1.5, 1.5, 2.5)
        glVertex3f(1.5, 0, 2.5)
        glEnd()
        
        # Front indicator (yellow stripe)
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(-1.5, 1.5, 2.5)
        glVertex3f(1.5, 1.5, 2.5)
        glVertex3f(1.5, 1.5, 3.0)
        glVertex3f(-1.5, 1.5, 3.0)
        glEnd()
        
        glPopMatrix()


class RaceGame:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Race Timmy - Drive the lap!")
        
        # Setup OpenGL
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.7, 1.0, 1.0)  # Sky blue background
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
        
        # Game objects
        self.track = Track()
        self.car = Car()
        self.lidar = LidarSensor()
        self.controller = CarController()
        
        # Game state
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.lap_time = None
        self.lap_count = 0
        
        # Camera control
        self.camera_distance = 40
        self.camera_angle = 0
        self.camera_height = 25
        self.mouse_dragging = False
        self.last_mouse_pos = None
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE:
                    self.paused = not self.paused
                elif event.key == K_r:
                    self.reset()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_dragging = True
                    self.last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up
                    self.camera_distance = max(10, self.camera_distance - 2)
                elif event.button == 5:  # Scroll down
                    self.camera_distance = min(100, self.camera_distance + 2)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
            elif event.type == MOUSEMOTION:
                if self.mouse_dragging and self.last_mouse_pos:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.camera_angle += dx * 0.5
                    self.camera_height = max(5, min(50, self.camera_height - dy * 0.2))
                    self.last_mouse_pos = event.pos
    
    def reset(self):
        """Reset the race"""
        self.car = Car()
        self.start_time = time.time()
        self.lap_time = None
        self.lap_count = 0
    
    def update(self, dt):
        """Update game state"""
        if self.paused:
            return
        
        # Get LIDAR data
        lidar_data = self.lidar.scan(self.car.pos, self.car.angle, self.track)
        
        # Call student's controller
        try:
            result = self.controller.control(lidar_data)
            if result is None:
                print("WARNING: controller.control() returned None!")
                acceleration, wheel_angle = 0, 0
            else:
                acceleration, wheel_angle = result
                # Debug output every 60 frames (once per second at 60fps)
                if int(time.time() * 60) % 60 == 0:
                    print(f"Controller: accel={acceleration:.1f}, wheel={wheel_angle:.1f}, speed={np.linalg.norm(self.car.velocity):.1f}")
        except Exception as e:
            print(f"Error in controller: {e}")
            import traceback
            traceback.print_exc()
            acceleration, wheel_angle = 0, 0
        
        # Clamp values
        self.car.acceleration = max(-10, min(10, acceleration))
        self.car.wheel_angle = max(-45, min(45, wheel_angle))
        
        # Update car
        old_pos = self.car.update(dt, self.track)
        
        # Check lap completion
        if old_pos is not None and self.track.check_lap_completion(old_pos, self.car.pos):
            if self.lap_count > 0:  # Don't count first crossing
                self.lap_time = time.time() - self.start_time
                self.paused = True
            self.lap_count += 1
    
    def render(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Camera follows car with mouse control
        angle_rad = math.radians(self.camera_angle)
        cam_x = self.car.pos[0] + self.camera_distance * math.sin(angle_rad)
        cam_z = self.car.pos[1] + self.camera_distance * math.cos(angle_rad)
        
        gluLookAt(
            cam_x, self.camera_height, cam_z,
            self.car.pos[0], 0, self.car.pos[1],
            0, 1, 0
        )
        
        # Draw ground (grass)
        glColor3f(0.2, 0.6, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-100, 0, -100)
        glVertex3f(100, 0, -100)
        glVertex3f(100, 0, 100)
        glVertex3f(-100, 0, 100)
        glEnd()
        
        # Draw track and car
        self.track.render()
        self.car.render()
        
        # Draw LIDAR visualization
        self._render_lidar()
        
        pygame.display.flip()
        
        # Draw 2D UI overlay
        self._render_ui()
    
    def _render_lidar(self):
        """Visualize LIDAR rays"""
        lidar_data = self.lidar.scan(self.car.pos, self.car.angle, self.track)
        
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        for i, distance in enumerate(lidar_data):
            angle_offset = self.lidar.angles[i]
            ray_angle = math.radians(self.car.angle + angle_offset)
            
            end_x = self.car.pos[0] + distance * math.cos(ray_angle)
            end_y = self.car.pos[1] + distance * math.sin(ray_angle)
            
            glVertex3f(self.car.pos[0], 0.5, self.car.pos[1])
            glVertex3f(end_x, 0.5, end_y)
        glEnd()
    
    def _render_ui(self):
        """Render 2D UI elements"""
        # Switch to 2D rendering
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        
        # Render text
        if self.lap_time:
            text = f"LAP COMPLETE! Time: {self.lap_time:.2f}s"
            color = (0, 255, 0)
        elif self.paused:
            text = "PAUSED - Press SPACE to continue"
            color = (255, 255, 0)
        else:
            elapsed = time.time() - self.start_time
            text = f"Time: {elapsed:.2f}s | Speed: {np.linalg.norm(self.car.velocity):.1f}"
            color = (255, 255, 255)
        
        text_surface = self.font.render(text, True, color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        
        glRasterPos2f(10, 30)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        # Instructions
        instructions = self.font.render("SPACE: Pause | R: Restart | ESC: Quit | MOUSE: Camera", True, (200, 200, 200))
        inst_data = pygame.image.tostring(instructions, "RGBA", True)
        glRasterPos2f(10, self.height - 40)
        glDrawPixels(instructions.get_width(), instructions.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, inst_data)
        
        # Restore 3D rendering
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()


if __name__ == "__main__":
    game = RaceGame()
    game.run()
