require_relative "cube.rb"

class Rubic < Cube
  def u
    tmp = [@rubic[0][0][0], @rubic[0][0][1], @rubic[0][0][2]]

    @rubic[0][0] = [@rubic[1][0][0], @rubic[1][0][1], @rubic[1][0][2]]
    @rubic[1][0] = [@rubic[2][0][0], @rubic[2][0][1], @rubic[2][0][2]]
    @rubic[2][0] = [@rubic[3][0][0], @rubic[3][0][1], @rubic[3][0][2]]
    @rubic[3][0] = [tmp[0], tmp[1], tmp[2]]
    rotate_inface(4)
  end

  def ui
    u
    u
    u
  end
end

