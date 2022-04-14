require 'colorize'

class Rubic

  def colorize(ok)
    if !!ok == ok
      @colorize = ok
    end
  end

  def numberize(ok)
    if !!ok == ok
      @numberize = ok
    end
  end

  def parse(file_name)
    ### ######## ##
    if (File.file?(file_name)) 
      print "File '#{file_name}' exists !\n\n"
    else
      print "File '#{file_name}' doesn't exist...\n"
    end

    file = File.open(file_name)
    content = file.read
    file.close

    lines = content.split("\n").map(&:split)
    
    cube = [lines[0..2]] + lines[3..5].map{ |x| x.each_slice(3).to_a}.transpose + [lines[6..8]]
    tmp = cube[0]
    cube[0] = cube[1]
    cube[1] = cube[2]
    cube[2] = cube[3]
    cube[3] = cube[4]
    cube[4] = tmp
    
    @rubic = cube
  end

  def random_generation
    print "No file given. Random generated map !"

  end

  def clear_generation
    print "No file given. Clear generated map !"
    @rubic = Array.new(6) {|i| Array.new(3, Array.new(3, i))}
  end

  def initialize(*args)
    case args.size
      when 0
        clear_generation
      when 1
        unless args[0].nil?
          parse(args[0])
        else
          clear_generation
        end
    end
    @colorized = false
    @numberize = true
  end

  def check
    return @rubic
  end

  def resolved
    if @rubic == Array.new(6) {|i| Array.new(3, Array.new(3, i))}
      true
    else
      false
    end
  end

  def rubic
    @rubic
  end

  # L'affichage du rubic

  def dump
    puts to_s
  end

  def to_s
    res = "      %d %d %d \n" % [@rubic[4][0][0], @rubic[4][0][1], @rubic[4][0][2]] +
    "      %d %d %d \n" % [@rubic[4][1][0], @rubic[4][1][1], @rubic[4][1][2]] +
    "      %d %d %d \n" % [@rubic[4][2][0], @rubic[4][2][1], @rubic[4][2][2]] +
    "%d %d %d %d %d %d %d %d %d %d %d %d \n" % [@rubic[0][0][0], @rubic[0][0][1], @rubic[0][0][2], @rubic[1][0][0], @rubic[1][0][1], @rubic[1][0][2], @rubic[2][0][0], @rubic[2][0][1], @rubic[2][0][2], @rubic[3][0][0], @rubic[3][0][1], @rubic[3][0][2]] +
    "%d %d %d %d %d %d %d %d %d %d %d %d \n" % [@rubic[0][1][0], @rubic[0][1][1], @rubic[0][1][2], @rubic[1][1][0], @rubic[1][1][1], @rubic[1][1][2], @rubic[2][1][0], @rubic[2][1][1], @rubic[2][1][2], @rubic[3][1][0], @rubic[3][1][1], @rubic[3][1][2]] +
    "%d %d %d %d %d %d %d %d %d %d %d %d \n" % [@rubic[0][2][0], @rubic[0][2][1], @rubic[0][2][2],@rubic[1][2][0], @rubic[1][2][1], @rubic[1][2][2],@rubic[2][2][0], @rubic[2][2][1], @rubic[2][2][2],@rubic[3][2][0], @rubic[3][2][1], @rubic[3][2][2]] +
    "      %d %d %d \n" % [@rubic[5][0][0], @rubic[5][0][1], @rubic[5][0][2]] + 
    "      %d %d %d \n" % [@rubic[5][1][0], @rubic[5][1][1], @rubic[5][1][2]] +
    "      %d %d %d \n" % [@rubic[5][2][0], @rubic[5][2][1], @rubic[5][2][2]] + "\n"

    if @colorize
      if @numberize
        vals = Array.new(6) {|x| x.to_s + ' '}
      else
        vals = Array.new(6, "  ")
      end
      res = res.gsub("0 ", vals[0].on_blue)
      res = res.gsub("1 ", vals[1].light_black.on_light_white)
      res = res.gsub("2 ", vals[2].on_green)
      res = res.gsub("3 ", vals[3].on_yellow)
      res = res.gsub("4 ", vals[4].on_red)
      res = res.gsub("5 ", vals[5].on_light_black)
    end

    res
  end

  # Mouvements

  def rotate_inface(face)
    tmp1 = @rubic[face][2][0]
    tmp2 = @rubic[face][2][1]
    
    @rubic[face][2][0] = @rubic[face][2][2]
    @rubic[face][2][1] = @rubic[face][1][2]

    @rubic[face][1][2] = @rubic[face][0][1]
    @rubic[face][2][2] = @rubic[face][0][2]
    
    @rubic[face][0][1] = @rubic[face][1][0]
    @rubic[face][0][2] = @rubic[face][0][0]

    @rubic[face][0][0] = tmp1
    @rubic[face][1][0] = tmp2

  end

  # F
  def f
    tmp = @rubic[4][2]

    @rubic[4][2] = [@rubic[0][2][2], @rubic[0][1][2], @rubic[0][0][2]]
  
    @rubic[0][0][2] = @rubic[5][0][0]
    @rubic[0][1][2] = @rubic[5][0][1]
    @rubic[0][2][2] = @rubic[5][0][2]

    @rubic[5][0] = [@rubic[2][2][0], @rubic[2][1][0], @rubic[2][0][0]]

    @rubic[2][0][0] = tmp[0]
    @rubic[2][1][0] = tmp[1]
    @rubic[2][2][0] = tmp[2]
    rotate_inface(1)

  end

  # F'
  def fp
    f
    f
    f
  end

  # R
  def r
    tmp = [@rubic[4][0][2], @rubic[4][1][2], @rubic[4][2][2]]

    @rubic[4][0][2] = @rubic[1][0][2]
    @rubic[4][1][2] = @rubic[1][1][2]
    @rubic[4][2][2] = @rubic[1][2][2]
    
    @rubic[1][0][2] = @rubic[5][0][2]
    @rubic[1][1][2] = @rubic[5][1][2]
    @rubic[1][2][2] = @rubic[5][2][2]

    @rubic[5][0][2] = @rubic[3][2][0]
    @rubic[5][1][2] = @rubic[3][1][0]
    @rubic[5][2][2] = @rubic[3][0][0]

    @rubic[3][0][0] = tmp[2]
    @rubic[3][1][0] = tmp[1]
    @rubic[3][2][0] = tmp[0]
    rotate_inface(2)
  end
  
  # R'
  def rp
    r
    r
    r
  end

  # U ##########
  def u
    tmp = @rubic[0][0]

    @rubic[0][0] = @rubic[1][0]
    @rubic[1][0] = @rubic[2][0]
    @rubic[2][0] = @rubic[3][0]
    @rubic[3][0] = tmp
    rotate_inface(4)
  end

  # U'
  def up
    u
    u
    u
  end
  
  # B
  def b
    tmp = @rubic[4][0]

    @rubic[4][0] = [@rubic[2][0][2], @rubic[2][1][2], @rubic[2][2][2]]
  
    @rubic[2][0][2] = @rubic[5][2][2]
    @rubic[2][1][2] = @rubic[5][2][1]
    @rubic[2][2][2] = @rubic[5][2][0]

    @rubic[5][2] = [@rubic[0][0][0], @rubic[0][1][0], @rubic[0][2][0]]

    @rubic[0][0][0] = tmp[2]
    @rubic[0][1][0] = tmp[1]
    @rubic[0][2][0] = tmp[0]
    rotate_inface(3)

  end

  # B'
  def bp
    b
    b
    b
  end

  # L
  def l
    lp
    lp
    lp
  end
  
  # L'
  def lp
    tmp = [@rubic[4][0][0], @rubic[4][1][0], @rubic[4][2][0]]

    @rubic[4][0][0] = @rubic[1][0][0]
    @rubic[4][1][0] = @rubic[1][1][0]
    @rubic[4][2][0] = @rubic[1][2][0]

    @rubic[1][0][0] = @rubic[5][0][0]
    @rubic[1][1][0] = @rubic[5][1][0]
    @rubic[1][2][0] = @rubic[5][2][0]

    @rubic[5][0][0] = @rubic[3][2][2]
    @rubic[5][1][0] = @rubic[3][1][2]
    @rubic[5][2][0] = @rubic[3][0][2]

    @rubic[3][0][2] = tmp[2]
    @rubic[3][1][2] = tmp[1]
    @rubic[3][2][2] = tmp[0]
    rotate_inface(0)
    rotate_inface(0)
    rotate_inface(0)
  end

  # D
  def d
    tmp = @rubic[3][2]

    @rubic[3][2] = @rubic[2][2]
    @rubic[2][2] = @rubic[1][2]
    @rubic[1][2] = @rubic[0][2]
    @rubic[0][2] = tmp
    rotate_inface(5)
  end

  # D'
  def dp
    d
    d
    d
  end

  def transform_left ##############
    d
    up
    
    tmp = @rubic[3][1]

    @rubic[3][1] = @rubic[2][1]
    @rubic[2][1] = @rubic[1][1]
    @rubic[1][1] = @rubic[0][1]
    @rubic[0][1] = tmp

  end

  def transform_right
    transform_left
    transform_left
    transform_left
  end

  def transform_up
    r
    lp
    
    tmp = [@rubic[4][0][1], @rubic[4][1][1], @rubic[4][2][1]]

    @rubic[4][0][1] = @rubic[1][0][1]
    @rubic[4][1][1] = @rubic[1][1][1]
    @rubic[4][2][1] = @rubic[1][2][1]
    
    @rubic[1][0][1] = @rubic[5][0][1]
    @rubic[1][1][1] = @rubic[5][1][1]
    @rubic[1][2][1] = @rubic[5][2][1]

    @rubic[5][0][1] = @rubic[3][2][1]
    @rubic[5][1][1] = @rubic[3][1][1]
    @rubic[5][2][1] = @rubic[3][0][1]

    @rubic[3][0][1] = tmp[2]
    @rubic[3][1][1] = tmp[1]
    @rubic[3][2][1] = tmp[0]
  end

  def transform_down
    transform_up
    transform_up
    transform_up
  end

end

